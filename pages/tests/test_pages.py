from __future__ import unicode_literals
from django.contrib.auth.models import AnonymousUser

from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.utils import translation

from pages.tests.base import PagesCase
from pages.models import PageSlugContent, PageMetaContent
from pages.models import PageRedirectContent
from pages.models import PageTextContent, PageMarkdownContent
from pages.models import PageImageContent
from pages.views import PageDetailsView


class TestPages(PagesCase):

    def test_page_slug_creation(self):
        self.slug = PageSlugContent.objects.create(page=self.page_foo, slug='test')

    def test_page_meta_creation(self):
        self.meta = PageMetaContent.objects.create(page=self.page_foo, title='test', description='test', keywords='test')

    def test_page_redirect_creation(self):
        self.redirect = PageRedirectContent.objects.create(page=self.page_foo)

    def test_page_text_creation(self):
        self.text = PageTextContent.objects.create(page=self.page_foo, text='test')

    def test_page_markdown_creation(self):
        self.markdown = PageMarkdownContent.objects.create(page=self.page_foo)

    def test_page_image_creation(self):
        self.image = PageImageContent.objects.create(page=self.page_foo)

    def test_page_view(self):
        PageSlugContent.objects.create(page=self.page_foo, slug='test')
        PageMetaContent.objects.create(page=self.page_foo, title='test', description='test', keywords='test')
        PageTextContent.objects.create(page=self.page_foo, text='test')
        page_url = reverse('page_show', kwargs={'slug': 'test'})
        request = self.factory.get(page_url)
        request.user = AnonymousUser()
        context = RequestContext(request)
        view = PageDetailsView.as_view()
        translation.activate('en')
        response = view(request=request, context=context, slug='test')
        translation.deactivate()
        self.assertEqual(response.status_code, 200)
