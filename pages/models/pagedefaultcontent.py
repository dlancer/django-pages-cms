"""Implements PageDefaultContent model"""

from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from pages.models.pagecontenttype import PageContentType


@python_2_unicode_compatible
class PageDefaultContent(models.Model):
    name = models.CharField(max_length=200, unique=True)
    content_types = models.CharField(max_length=254)
    objects = models.Manager()

    def __str__(self):
        """id string of instance"""
        return '{0}'.format(self.name)

    def get_content_types(self):
        content_types = []
        ctypes = self.content_types.split(':')
        for ctype in ctypes:
            try:
                pctype = PageContentType.objects.get(type=ctype)
                content_types.append(pctype)
            except PageContentType.DoesNotExist:
                pass
        return content_types

    def save(self, *args, **kwargs):
        """Override the default ``save`` method."""

        # Call parent's ``save`` method
        super(PageDefaultContent, self).save(*args, **kwargs)

    class Meta:
        app_label = 'pages'
        verbose_name = _('Default Content')
        verbose_name_plural = _('Default Content')
