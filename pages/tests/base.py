from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import RequestFactory
from django.contrib.sites.models import Site

from pages.models.page import Page


class PagesCase(TestCase):
    urls = 'pages.tests.urls'
    fixtures = ['fixtures/pages_testdata.yaml']

    def setUp(self):
        self.factory = RequestFactory()
        self.site_foo = Site.objects.get(id=1)
        self.user_foo = User.objects.create(username='foo', password='bar', email='foo@test.com')
        self.page_foo = Page.objects.create(name='Test', created_by=self.user_foo,
                                            updated_by=self.user_foo, is_draft=False, is_published=True)
        self.page_foo2 = Page.objects.create(name='Test2', created_by=self.user_foo,
                                             updated_by=self.user_foo, is_draft=False, is_published=True)
        self.page_foo3 = Page.objects.create(name='Test3', created_by=self.user_foo,
                                             updated_by=self.user_foo, is_draft=False, is_published=True)
        self.page_foo4 = Page.objects.create(name='Test4', created_by=self.user_foo,
                                             updated_by=self.user_foo, is_draft=False, is_published=True)
        self.page_foo5 = Page.objects.create(name='Test5', created_by=self.user_foo,
                                             updated_by=self.user_foo, is_draft=False, is_published=True)
        self.page_foo6 = Page.objects.create(name='Test6', created_by=self.user_foo,
                                             updated_by=self.user_foo, is_draft=False, is_published=True)

    def tearDown(self):
        self.user_foo.delete()
