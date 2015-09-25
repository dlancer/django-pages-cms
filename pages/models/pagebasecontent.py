"""Implements PageBaseContent model"""

from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible

from pages.conf import settings
from pages.models.pagecontenttype import get_all_content_tuple


@python_2_unicode_compatible
class PageBaseContent(models.Model):
    type = models.CharField(_('Type'), choices=get_all_content_tuple(), max_length=100, blank=False, db_index=True)
    page = models.ForeignKey('pages.Page', verbose_name=_('Page'))
    language = models.CharField(max_length=5, default=str(settings.PAGES_DEFAULT_LANGUAGE))
    sid = models.CharField(max_length=200, unique=True)
    name = models.CharField(max_length=200, blank=True, unique=True)
    is_extended = models.BooleanField(_('Extended?'), default=False)
    comment = models.CharField(max_length=250, blank=True)
    date_created = models.DateTimeField(_('Created'), default=timezone.now)
    date_updated = models.DateTimeField(_('Updated'), default=timezone.now)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='%(app_label)s_%(class)s_creator', null=True
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='%(app_label)s_%(class)s_editor', null=True
    )

    def __str__(self):
        """id string of instance"""
        return '{0:>s}'.format(self.sid)

    def count_objects(self, use_lang=True):
        if use_lang:
            count = self.__class__.objects.filter(page=self.page, language=self.language).count()
        else:
            count = self.__class__.objects.filter(page=self.page).count()
        return count

    def update_fields(self, change):
        pass

    def save(self, *args, **kwargs):
        """Override the default ``save`` method."""

        if self.pk is None:
            self.created_by = self.page.created_by
            self.update_fields(False)
            count = self.count_objects() + 1
        else:
            self.update_fields(True)
            count = int(self.sid.split(':')[-1])
        self.sid = '{0:>s}:{1:>s}:{2:>s}:{3:>d}'.format(self.language, self.page.name, self.type, count)
        self.name = self.name if len(self.name) else self.sid
        self.updated_by = self.page.updated_by

        # Call parent's ``save`` method
        super(PageBaseContent, self).save(*args, **kwargs)

    class Meta:
        abstract = True

    class PageMeta:
        def __init__(self):
            self.context_name = 'base'
            self.multiple_per_page = True
            self.multiple_per_locale = True
