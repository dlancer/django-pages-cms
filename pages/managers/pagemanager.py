import django

from django.db import models

from pages.conf import settings


class PageManager(models.Manager):
    def get_queryset(self):
        super_ = super(PageManager, self)
        # fix get_query_set for old Django releases
        if django.VERSION < (1, 6):
            qs = super_.get_query_set()
        else:
            qs = super_.get_queryset()

        # Restrict operations to pages on the current site if needed
        if settings.PAGES_HIDE_SITES and settings.PAGES_USE_SITE_ID:
            return qs.filter(sites=settings.SITE_ID)
        else:
            return qs

    get_query_set = get_queryset

    def get_queryset_compat(self):
        get_queryset = (self.get_query_set if hasattr(self, 'get_query_set') else self.get_queryset)
        return get_queryset()

    def on_site(self, site_id=None):
        """Return a :class:`QuerySet` of pages that are published on the site
        defined by the ``SITE_ID`` setting.

        :param site_id: specify the id of the site object to filter with.
        """
        if settings.PAGES_USE_SITE_ID:
            if not site_id:
                site_id = settings.SITE_ID
            return self.get_queryset_compat().filter(sites=site_id)
        return self.all()

    def published(self):
        """Return queryset with only published pages"""
        return self.get_queryset_compat().filter(is_published=True, is_hidden=False)
