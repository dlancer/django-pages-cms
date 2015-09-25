"""Implements PageContent model"""

from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _


from pages.models import Page
from pages.models.pagecontenttype import PageContentType


@python_2_unicode_compatible
class PageContent(models.Model):
    page = models.ForeignKey(Page, verbose_name=_('Page'))
    type = models.ForeignKey(PageContentType)
    objects = models.Manager()

    def __str__(self):
        """id string of instance"""
        return '{0}:{1}:{2}'.format(self.page, self.type, self.pk)

    def save(self, *args, **kwargs):
        """Override the default ``save`` method."""

        # Call parent's ``save`` method
        super(PageContent, self).save(*args, **kwargs)

    class Meta:
        app_label = 'pages'
        verbose_name = _('Content')
        verbose_name_plural = _('Content')
        unique_together = ('page', 'type',)
