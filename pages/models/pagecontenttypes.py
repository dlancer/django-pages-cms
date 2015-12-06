"""Implements page content models"""

from __future__ import unicode_literals
import hashlib
import os
import base64
import uuid
import importlib
import slugify

from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

from image_cropping import ImageCropField
from image_cropping import ImageRatioField
from markitup.fields import MarkupField

from pages.conf import settings
from pages.models.pagebasecontent import PageBaseContent
from pages.storage import PageFileSystemStorage


PAGE_EXT_CONTENT_TYPES = []

if settings.PAGES_PAGE_USE_EXT_CONTENT_TYPES:
    if settings.PAGES_PAGE_EXT_CONTENT_TYPES is not None:
        try:
            for content_type in settings.PAGES_PAGE_EXT_CONTENT_TYPES:
                PAGE_EXT_CONTENT_TYPES.append(importlib.import_module(content_type))
        except ImportError as e:
            raise Exception('Extended content type import error: {0}'.format(e))


class PageSlugContent(PageBaseContent):
    slug = models.CharField(max_length=245)
    objects = models.Manager()

    @property
    def full_slug(self):
        return self.language + '/' + self.slug

    def update_fields(self, change):
        if not change:
            self.type = 'slug'
        if not self.slug:
            self.slug = slugify.slugify(self.page.name,
                                        only_ascii=settings.PAGES_PAGE_ONLY_ASCII_SLUGS)
        else:
            self.slug = slugify.slugify(self.slug,
                                        only_ascii=settings.PAGES_PAGE_ONLY_ASCII_SLUGS)

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


image_file_storage = PageFileSystemStorage()


def make_image_upload_path(instance, filename, prefix=False):
    """Generate upload path and filename for image"""

    # store original filename
    instance.filename = filename
    ext = os.path.splitext(filename)[1].strip('.').lower()

    # always generate unique path, for security and file system balancing reasons
    file_uuid = uuid.uuid4().hex

    # generate short sha1 based hash
    name_sha = hashlib.sha1(file_uuid).digest()
    name_hash = base64.urlsafe_b64encode(name_sha[:9]).decode('utf-8')

    if settings.PAGES_IMAGE_USE_ORIGINAL_FILENAME:
        name = image_file_storage.get_available_name(os.path.splitext(filename)[0])
    else:
        name = name_hash

    return u'{path}/{sub0}/{sub1}/{sub2}/{name}.{ext}'.format(
        path=settings.PAGES_IMAGE_DIR,
        sub0=file_uuid[0:2],
        sub1=file_uuid[7:9],
        sub2=file_uuid[12:14],
        name=name,
        ext=ext
    )


class PageImageContent(PageBaseContent):
    image = ImageCropField(blank=True, null=True, upload_to=make_image_upload_path, storage=image_file_storage)
    cropping = ImageRatioField('image', '{0:>s}x{1:>s}'.format(
        str(settings.PAGES_IMAGE_WIDTH_MAX), str(settings.PAGES_IMAGE_HEIGHT_MAX)), allow_fullsize=True)
    title = models.CharField(max_length=250, blank=True)
    tags = models.CharField(max_length=250, blank=True)
    objects = models.Manager()

    def update_fields(self, change):
        if not change:
            self.type = 'image'

    def image_cropping_link(self):
        """Return image cropping link"""
        change_url = reverse('admin:pages_pageimagecontent_change', args=(self.id,))
        return '<a href="{0:>s}" onclick="return showAddAnotherPopup(this);">{1:>s}</a>'.format(change_url, _('CROP'))

    image_cropping_link.short_description = _('Cropping')
    image_cropping_link.allow_tags = True

    class Meta(PageBaseContent.Meta):
        app_label = 'pages'
        verbose_name = _('Image')
        verbose_name_plural = _('Images')

    class PageMeta(PageBaseContent.PageMeta):
        context_name = 'images'
        multiple_per_page = True
        multiple_per_locale = True


# Signals handler for deleting files after object record deleted
@receiver(post_delete, sender=PageImageContent)
def delete_image(sender, **kwargs):
    """Automatically delete image file when records removed."""
    if settings.PAGES_DELETE_IMAGE_FILE:
        image = kwargs.get('instance')
        if image.image is not None:
            try:
                image.image.storage.delete(image.image.path)
            except Exception:
                pass
