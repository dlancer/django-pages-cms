"""Implements page video extended content model"""

from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _

from pages.conf import settings
from pages.models.pagebasecontent import PageBaseContent

if settings.PAGES_PAGE_USE_EXT_CONTENT_TYPES:
    from embed_video.fields import EmbedVideoField

    class PageVideoContent(PageBaseContent):
        video = EmbedVideoField(blank=True)
        title = models.CharField(max_length=160, blank=True)
        description = models.TextField(max_length=160, blank=True)
        objects = models.Manager()

        def update_fields(self, change):
            if not change:
                self.type = 'video'
                self.is_extended = True

        class Meta(PageBaseContent.Meta):
            app_label = 'extpages'
            verbose_name = _('Video')
            verbose_name_plural = _('Video')

        class PageMeta(PageBaseContent.PageMeta):
            context_name = 'video'
            multiple_per_page = True
            multiple_per_locale = True
