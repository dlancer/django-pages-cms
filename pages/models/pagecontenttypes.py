"""Implements page content models"""

from __future__ import unicode_literals
import importlib
import slugify
import itertools

from django.db import models
from django.utils.translation import ugettext_lazy as _

from markitup.fields import MarkupField

from pages.conf import settings
from pages.models.pagebasecontent import PageBaseContent

PAGE_EXT_CONTENT_TYPES = []
PAGE_MAX_SLUG_LENGTH = 245

if settings.PAGES_PAGE_USE_EXT_CONTENT_TYPES:
    if settings.PAGES_PAGE_EXT_CONTENT_TYPES is not None:
        try:
            for content_type in settings.PAGES_PAGE_EXT_CONTENT_TYPES:
                PAGE_EXT_CONTENT_TYPES.append(importlib.import_module(content_type))
        except ImportError as e:
            from django.core.exceptions import ImproperlyConfigured
            raise ImproperlyConfigured('Extended content type import error: {0}'.format(e))


class PageSlugContent(PageBaseContent):
    slug = models.CharField(max_length=PAGE_MAX_SLUG_LENGTH)
    objects = models.Manager()

    @property
    def full_slug(self):
        return self.language + '/' + self.slug

    def update_fields(self, change):
        if not change:
            self.type = 'slug'

    def save(self, *args, **kwargs):
        title = self.slug
        if not len(title):
            if settings.PAGES_PAGE_USE_META_TITLE_FOR_SLUG:
                try:
                    meta = PageMetaContent.objects.get(page=self.page, language=self.language)
                    title = meta.title
                except PageMetaContent.DoesNotExist:
                    pass
            else:
                title = self.page.name
        self.slug = orig = slugify.slugify(title)[:PAGE_MAX_SLUG_LENGTH]
        for x in itertools.count(1):
            if not PageSlugContent.objects.exclude(
                    page=self.page
            ).filter(slug=self.slug, language=self.language).exists():
                break
            self.slug = '{0:s}-{1:d}'.format(orig[:PAGE_MAX_SLUG_LENGTH - len(str(x)) - 1], x)
        super(PageSlugContent, self).save(*args, **kwargs)

    class Meta(PageBaseContent.Meta):
        app_label = 'pages'
        verbose_name = _('Slug')
        verbose_name_plural = _('Slugs')
        unique_together = ('language', 'page',)

    class PageMeta(PageBaseContent.PageMeta):
        context_name = 'slug'
        multiple_per_page = True
        multiple_per_locale = False


class PageRedirectContent(PageBaseContent):
    redirect_to_page = models.CharField(max_length=254, null=True, blank=True)
    redirect_to_url = models.URLField(max_length=254, null=True, blank=True)
    is_permanent = models.BooleanField(_('Permanent'), default=False)

    def update_fields(self, change):
        if not change:
            self.type = 'redirect'

    def get_redirect_url(self, request):
        url = None
        if self.redirect_to_page:
            url = request.build_absolute_uri(self.redirect_to_page)
        else:
            if self.redirect_to_url:
                url = self.redirect_to_url
        return url

    class Meta(PageBaseContent.Meta):
        app_label = 'pages'
        verbose_name = _('Redirect')
        verbose_name_plural = _('Redirect')

    class PageMeta(PageBaseContent.PageMeta):
        context_name = 'redirect'
        multiple_per_page = True
        multiple_per_locale = False


class PageMetaContent(PageBaseContent):
    title = models.CharField(max_length=160, blank=True)
    description = models.TextField(max_length=160, blank=True)
    keywords = models.CharField(max_length=200, blank=True)
    is_noindex = models.BooleanField(_('NoIndex'), default=False)
    is_nofollow = models.BooleanField(_('NoFollow'), default=False)
    objects = models.Manager()

    def update_fields(self, change):
        if not change:
            self.type = 'meta'

    @property
    def robots(self):
        """Return values for robots html meta key"""
        r = 'noindex' if self.is_noindex else 'index'
        r += ','
        r += 'nofollow' if self.is_nofollow else 'follow'
        return r

    class Meta(PageBaseContent.Meta):
        app_label = 'pages'
        verbose_name = _('Meta')
        verbose_name_plural = _('Meta')
        unique_together = ('language', 'page',)

    class PageMeta(PageBaseContent.PageMeta):
        context_name = 'meta'
        multiple_per_page = True
        multiple_per_locale = False


class PageTextContent(PageBaseContent):
    text = models.TextField(blank=True)
    is_template = models.BooleanField(_('Template?'), default=False)
    objects = models.Manager()

    def update_fields(self, change):
        if not change:
            self.type = 'text'

    class Meta(PageBaseContent.Meta):
        app_label = 'pages'
        verbose_name = _('Text')
        verbose_name_plural = _('Text')

    class PageMeta(PageBaseContent.PageMeta):
        context_name = 'text'
        multiple_per_page = True
        multiple_per_locale = True


class PageMarkdownContent(PageBaseContent):
    text = MarkupField(blank=True)
    is_template = models.BooleanField(_('Template?'), default=False)
    objects = models.Manager()

    def update_fields(self, change):
        if not change:
            self.type = 'markdown'

    class Meta(PageBaseContent.Meta):
        app_label = 'pages'
        verbose_name = _('Markdown')
        verbose_name_plural = _('Markdown')

    class PageMeta(PageBaseContent.PageMeta):
        context_name = 'markdown'
        multiple_per_page = True
        multiple_per_locale = True
