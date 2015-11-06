# -*- coding: utf-8
from __future__ import unicode_literals
from django.contrib.auth.models import AnonymousUser
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.utils import translation

from pages.cache import cache
from pages.conf import settings
from pages.tests.base import PagesCase
from pages.models import PageSlugContent, PageMetaContent
from pages.models import PageRedirectContent
from pages.models import PageTextContent, PageMarkdownContent
from pages.models import PageImageContent
from pages.views import PageDetailsView


class TestPages(PagesCase):

    def test_page_slug_model(self):
        PageSlugContent.objects.create(page=self.page_foo, slug='test')
        obj = PageSlugContent.objects.filter(page=self.page_foo, language='en', slug='test')[0]
        sid = obj.sid
        self.assertEqual(sid, 'en:Test:slug:1')
        obj.language = 'de'
        obj.save()
        self.assertEqual(obj.sid, 'de:Test:slug:1')

    def test_page_meta_model(self):
        PageMetaContent.objects.create(page=self.page_foo, title='test', description='test', keywords='test')
        obj = PageMetaContent.objects.filter(page=self.page_foo, language='en')[0]
        sid = obj.sid
        self.assertEqual(sid, 'en:Test:meta:1')
        obj.language = 'de'
        obj.save()
        self.assertEqual(obj.sid, 'de:Test:meta:1')

    def test_page_redirect_model(self):
        PageRedirectContent.objects.create(page=self.page_foo)
        obj = PageRedirectContent.objects.filter(page=self.page_foo, language='en')[0]
        sid = obj.sid
        self.assertEqual(sid, 'en:Test:redirect:1')
        obj.language = 'de'
        obj.save()
        self.assertEqual(obj.sid, 'de:Test:redirect:1')

    def test_page_text_model(self):
        PageTextContent.objects.create(page=self.page_foo, text='test')
        obj = PageTextContent.objects.filter(page=self.page_foo, language='en')[0]
        sid = obj.sid
        self.assertEqual(sid, 'en:Test:text:1')
        obj.language = 'de'
        obj.save()
        self.assertEqual(obj.sid, 'de:Test:text:1')

    def test_page_markdown_model(self):
        PageMarkdownContent.objects.create(page=self.page_foo)
        obj = PageMarkdownContent.objects.filter(page=self.page_foo, language='en')[0]
        sid = obj.sid
        self.assertEqual(sid, 'en:Test:markdown:1')
        obj.language = 'de'
        obj.save()
        self.assertEqual(obj.sid, 'de:Test:markdown:1')

    def test_page_image_model(self):
        PageImageContent.objects.create(page=self.page_foo)
        obj = PageImageContent.objects.filter(page=self.page_foo, language='en')[0]
        sid = obj.sid
        self.assertEqual(sid, 'en:Test:image:1')
        obj.language = 'de'
        obj.save()
        self.assertEqual(obj.sid, 'de:Test:image:1')

    def test_page_absolute_url(self):
        PageSlugContent.objects.create(page=self.page_foo, slug='test')
        PageMetaContent.objects.create(page=self.page_foo, title='test', description='test', keywords='test')
        PageTextContent.objects.create(page=self.page_foo, text='test')
        self.page_foo.template = 'pages/page_text.html'
        self.page_foo.save()
        page_url = self.page_foo.get_absolute_url()
        self.assertEqual(page_url, '/page/test/')
        self.page_foo.delete()
        cache.clear()

    def test_page_text_view(self):
        PageSlugContent.objects.create(page=self.page_foo, slug='test')
        PageMetaContent.objects.create(page=self.page_foo, title='test', description='test', keywords='test')
        PageTextContent.objects.create(page=self.page_foo, text='test')
        self.page_foo.template = 'pages/page_text.html'
        self.page_foo.save()
        page_url = reverse('page_show', kwargs={'slug': 'test'})
        request = self.factory.get(page_url)
        request.user = AnonymousUser()
        context = RequestContext(request)
        view = PageDetailsView.as_view()
        translation.activate('en')
        response = view(request=request, context=context, slug='test')
        translation.deactivate()
        self.assertEqual(response.status_code, 200)
        self.page_foo.delete()
        cache.clear()

    def test_page_text_view_cache(self):
        PageSlugContent.objects.create(page=self.page_foo, slug='test')
        PageMetaContent.objects.create(page=self.page_foo, title='test', description='test', keywords='test')
        PageTextContent.objects.create(page=self.page_foo, text='test')
        self.page_foo.template = 'pages/page_text.html'
        self.page_foo.save()
        page_url = reverse('page_show', kwargs={'slug': 'test'})
        request = self.factory.get(page_url)
        request.user = AnonymousUser()
        context = RequestContext(request)
        view = PageDetailsView.as_view()
        translation.activate('en')
        response = view(request=request, context=context, slug='test')
        translation.deactivate()
        self.assertEqual(response.status_code, 200)
        page_cache_key = settings.PAGES_PAGE_CACHE_KEY + 'en' + ':' + 'test' + ':' + 'False'
        page_cache_version_key = settings.PAGES_PAGE_VERSION_KEY + 'en' + ':' + 'test'
        cache_version = cache.get(page_cache_version_key)
        page = cache.get(page_cache_key, version=cache_version)
        self.assertNotEqual(page, None)
        self.page_foo.save()
        cache_version = cache.get(page_cache_version_key)
        self.assertEqual(cache_version, 2)
        self.page_foo.delete()
        cache.clear()

    def test_page_markdown_view(self):
        PageSlugContent.objects.create(page=self.page_foo, slug='test')
        PageMetaContent.objects.create(page=self.page_foo, title='test', description='test', keywords='test')
        PageMarkdownContent.objects.create(page=self.page_foo, text='**test**')
        self.page_foo.template = 'pages/page_markdown.html'
        self.page_foo.save()
        page_url = reverse('page_show', kwargs={'slug': 'test'})
        request = self.factory.get(page_url)
        request.user = AnonymousUser()
        context = RequestContext(request)
        view = PageDetailsView.as_view()
        translation.activate('en')
        response = view(request=request, context=context, slug='test')
        translation.deactivate()
        self.assertEqual(response.status_code, 200)
        self.page_foo.delete()
        cache.clear()

    def test_page_image_view(self):
        PageSlugContent.objects.create(page=self.page_foo, slug='test')
        PageMetaContent.objects.create(page=self.page_foo, title='test', description='test', keywords='test')
        PageTextContent.objects.create(page=self.page_foo, text='test')
        PageImageContent.objects.create(page=self.page_foo, image='img/test.jpg', title='test')
        self.page_foo.template = 'pages/page_image.html'
        self.page_foo.save()
        page_url = reverse('page_show', kwargs={'slug': 'test'})
        request = self.factory.get(page_url)
        request.user = AnonymousUser()
        context = RequestContext(request)
        view = PageDetailsView.as_view()
        translation.activate('en')
        response = view(request=request, context=context, slug='test')
        translation.deactivate()
        self.assertEqual(response.status_code, 200)
        self.page_foo.delete()
        cache.clear()

    def test_page_with_non_ascii_slug(self):
        PageSlugContent.objects.create(page=self.page_foo, slug='prüfung')
        PageMetaContent.objects.create(page=self.page_foo, title='test', description='test', keywords='test')
        PageTextContent.objects.create(page=self.page_foo, text='test')
        self.page_foo.template = 'pages/page_text.html'
        self.page_foo.save()
        page_url = reverse('page_show', kwargs={'slug': 'prüfung'})
        request = self.factory.get(page_url)
        request.user = AnonymousUser()
        context = RequestContext(request)
        view = PageDetailsView.as_view()
        translation.activate('en')
        response = view(request=request, context=context, slug='prüfung')
        translation.deactivate()
        self.assertEqual(response.status_code, 200)
        self.page_foo.delete()
        cache.clear()

    def test_page_fallback_language(self):
        PageSlugContent.objects.create(page=self.page_foo, slug='test')
        PageMetaContent.objects.create(page=self.page_foo, title='test', description='test', keywords='test')
        PageTextContent.objects.create(page=self.page_foo, text='test')
        self.page_foo.template = 'pages/page_text.html'
        self.page_foo.save()
        page_url = '/de' + reverse('page_show', kwargs={'slug': 'test'})
        request = self.factory.get(page_url)
        request.user = AnonymousUser()
        context = RequestContext(request)
        view = PageDetailsView.as_view()
        translation.activate('de')
        response = view(request=request, context=context, slug='test')
        self.assertEqual(response.status_code, 302)
        page_url = response.get('location')
        response = self.client.get(page_url)
        translation.deactivate()
        self.assertEqual(response.status_code, 200)
        self.page_foo.delete()
        cache.clear()
