"""Implements PageContentType model"""

from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from pages.managers import ContentTypeManager


def get_all_content_tuple():
    content_types = []
    try:
        types = PageContentType.objects.all()
        for i in types:
            content_types.append((i.type, i.type))
    except Exception:
        # Probably PageContentType table not populated.
        pass
    return tuple(content_types)


@python_2_unicode_compatible
class PageContentType(models.Model):
    type = models.CharField(_('Type'), max_length=100, blank=False)
    class_name = models.CharField(_('Class'), max_length=100, blank=False)
    admin_class_name = models.CharField(_('Admin Class'), max_length=100, blank=False)
    is_extended = models.BooleanField('Extended', default=False)
    objects = ContentTypeManager()

    def __str__(self):
        """id string of instance"""
        return '{0}'.format(self.type)

    class Meta:
        app_label = 'pages'
        verbose_name = _('Content Type')
        verbose_name_plural = _('Content Types')
