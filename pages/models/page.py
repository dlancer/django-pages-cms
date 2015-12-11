"""Implements Page models"""

from __future__ import unicode_literals

from django.db import models
from django.db.models import Q
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.utils.encoding import python_2_unicode_compatible
from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import iri_to_uri
from django.utils.translation import get_language

from mptt.models import MPTTModel, TreeForeignKey
from guardian.models import UserObjectPermissionBase
from guardian.models import GroupObjectPermissionBase
from guardian.models import UserObjectPermission
from guardian.models import GroupObjectPermission

from pages.conf import settings
from pages.cache import cache
from pages.managers import PageManager
from pages.models.pagecontenttype import PageContentType
from pages.models import pagecontenttypes


@python_2_unicode_compatible
class Page(MPTTModel):
    name = models.CharField(max_length=200, unique=True)
    ptype = models.CharField(_('Type'), max_length=64, default='page')
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')
    template = models.CharField(max_length=254, blank=True)
    comment = models.TextField(max_length=254, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='page_creator', null=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='page_editor', null=True)
    date_created = models.DateTimeField(_('Created'), default=timezone.now)
    date_updated = models.DateTimeField(_('Updated'), default=timezone.now)
    date_approved = models.DateTimeField(_('Approved'), null=True, blank=True)
    date_publication = models.DateTimeField(_('Publication date'), null=True, blank=True)
    date_publication_end = models.DateTimeField(_('Publication end date'), null=True, blank=True)
    is_draft = models.BooleanField(_('Draft'), default=True)
    is_approved = models.BooleanField(_('Approved'), default=False)
    is_hidden = models.BooleanField(_('Hidden'), default=False)
    is_published = models.BooleanField(_('Published'), default=False)
    is_login_required = models.BooleanField(_('Login required'), default=False)
    is_permission_required = models.BooleanField(_('Permission required'), default=False)
    sites = models.ManyToManyField(Site, help_text=_('The site(s) where this pages is accessible.'),
                                   verbose_name=_('sites'))
    objects = PageManager()

    def __init__(self, *args, **kwargs):
        """Instantiate the pages object."""
        # per instance cache
        self._languages = None
        self._content = None
        self._is_first_root = None
        super(Page, self).__init__(*args, **kwargs)

    def __str__(self):
        """id string of instance"""
        return self.name

    def get_absolute_url(self):
        """absolute url of instance"""
        content = self.get_content('slug')
        language = get_language()
        slug = None
        for obj in content:
            if obj.language == language:
                slug = obj.slug
                break
        url = iri_to_uri(reverse('page_show', args=(slug,)))
        return url

    def save(self, *args, **kwargs):
        """Override the default ``save`` method."""

        now = timezone.now()

        # update pages status flags
        if self.is_approved:
            self.is_draft = False
            # Published pages should always have a publication date
            if self.date_publication is None and not self.is_draft:
                self.date_publication = now
            if self.date_publication > now:
                self.is_published = True
            if self.date_publication_end is not None:
                if self.date_publication_end < now:
                    self.is_hidden = True
            if self.date_approved is None:
                self.date_approved = now
        else:
            if self.date_approved is not None:
                self.date_approved = None

        self.date_updated = now

        if self.template is not None:
            self.template = self.template.strip()

        # Call parent's ``save`` method
        super(Page, self).save(*args, **kwargs)

    @property
    def is_visible(self):
        """Return True if page is visible"""
        now = timezone.now()
        if self.date_publication_end:
            publication = self.date_publication < now < self.date_publication_end
        else:
            publication = self.date_publication < now
        return not self.is_draft and not self.hidden and self.is_approved and publication

    def invalidate(self):
        content = self.get_content('slug')
        for obj in content:
            cache_key = settings.PAGES_PAGE_CACHE_KEY + obj.language + ':' + obj.slug
            cache_key_version = settings.PAGES_PAGE_VERSION_KEY + obj.language + ':' + obj.slug
            cache_version = str(cache.get(cache_key_version))
            if cache_version is None:
                cache.set(cache_key_version, 1, settings.PAGES_PAGE_CACHE_TIMEOUT)
                cache_version = 1
            try:
                cache.incr(cache_key_version, 1)
                if settings.PAGES_CACHE_DELETE:
                    # try delete cache for anonymous and authenticated users
                    cache_key_yauth = cache_key + ':' + 'True'
                    cache_key_nauth = cache_key + ':' + 'False'
                    cache.delete(cache_key_yauth, version=cache_version)
                    cache.delete(cache_key_nauth, version=cache_version)
                    cache.delete(cache_key_yauth + 'content', version=cache_version)
                    cache.delete(cache_key_nauth + 'content', version=cache_version)
                    cache.delete(cache_key_yauth + 'ext_content', version=cache_version)
                    cache.delete(cache_key_nauth + 'ext_content', version=cache_version)
                    cache.delete(cache_key_yauth + 'redirect', version=cache_version)
                    cache.delete(cache_key_nauth + 'redirect', version=cache_version)
            except ValueError:
                cache.set(cache_key_version, 1, settings.PAGES_PAGE_CACHE_TIMEOUT)

    @staticmethod
    def get_content_class(content_type):
        content_class = None
        content_type = PageContentType.objects.get(type=content_type)
        if content_type:
            try:
                content_class = getattr(pagecontenttypes, content_type.class_name)
                if not issubclass(content_class, pagecontenttypes.PageBaseContent):
                    content_class = None
            except AttributeError:
                if settings.PAGES_PAGE_USE_EXT_CONTENT_TYPES:
                    if pagecontenttypes.PAGE_EXT_CONTENT_TYPES is not None:
                        for module in pagecontenttypes.PAGE_EXT_CONTENT_TYPES:
                            if hasattr(module, content_type.class_name):
                                content_class = getattr(module, content_type.class_name)
                                if not issubclass(content_class, pagecontenttypes.PageBaseContent):
                                    content_class = None
                                break
        return content_class

    def get_template(self):
        return self.template if self.template else settings.PAGES_DEFAULT_TEMPLATE

    def get_content(self, content_type, language=None):
        content_class = self.get_content_class(content_type=content_type)
        if language is None:
            content = content_class.objects.filter(page=self.pk)
        else:
            content = content_class.objects.filter(page=self.pk, language=language)
        return content

    class Meta:
        ordering = ['tree_id', 'lft']
        get_latest_by = 'date_publication'
        app_label = 'pages'
        verbose_name = _('Page')
        verbose_name_plural = _('Pages')
        permissions = (
            ('view_page', _('Can view pages')),
        )

    class MPTTMeta:
        order_insertion_by = ['name']


@receiver(post_save, sender=Page)
def on_save(sender, instance, using, **kwargs):
    if isinstance(instance, Page):
        instance.invalidate()


@receiver(pre_delete, sender=Page)
def on_delete(sender, instance, using, **kwargs):
    if isinstance(instance, Page):
        instance.invalidate()


class PageUserObjectPermission(UserObjectPermissionBase):
    content_object = models.ForeignKey(Page)

    class Meta:
        app_label = 'pages'
        verbose_name = _('Page User Permissions')
        verbose_name_plural = _('Pages Users Permissions')


class PageGroupObjectPermission(GroupObjectPermissionBase):
    content_object = models.ForeignKey(Page)

    class Meta:
        app_label = 'pages'
        verbose_name = _('Page Group Permissions')
        verbose_name_plural = _('Pages Groups Permissions')


def remove_obj_perms_connected_with_user(sender, instance, **kwargs):
    filters = Q(content_type=ContentType.objects.get_for_model(instance), object_pk=instance.pk)
    UserObjectPermission.objects.filter(filters).delete()
    GroupObjectPermission.objects.filter(filters).delete()


pre_delete.connect(remove_obj_perms_connected_with_user, sender=settings.AUTH_USER_MODEL)
