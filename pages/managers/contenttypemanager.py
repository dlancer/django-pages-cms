import django
from django.db import models

from pages.conf import settings


class ContentTypeManager(models.Manager):

    def get_queryset(self):
        super_ = super(ContentTypeManager, self)
        # fix get_query_set for old Django releases
        if django.VERSION < (1, 6):
            qs = super_.get_query_set()
        else:
            qs = super_.get_queryset()
        if not settings.PAGES_PAGE_USE_EXT_CONTENT_TYPES:
            return qs.filter(is_extended=False)
        else:
            return qs

    get_query_set = get_queryset

    def get_queryset_compat(self):
        get_queryset = (self.get_query_set if hasattr(self, 'get_query_set') else self.get_queryset)
        return get_queryset()

    def extended(self):
        """Return queryset with only extended content types"""
        return self.get_queryset_compat().filter(is_extended=True)
