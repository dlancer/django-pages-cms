from django.db import models

from pages.conf import settings


class PageManager(models.Manager):
    if settings.PAGES_HIDE_SITES and settings.PAGES_USE_SITE_ID:
        def get_query_set(self):
            """Restrict operations to pages on the current site."""
            return super(PageManager, self).get_query_set().filter(
                sites=settings.SITE_ID)

    def on_site(self, site_id=None):
        """Return a :class:`QuerySet` of pages that are published on the site
        defined by the ``SITE_ID`` setting.

        :param site_id: specify the id of the site object to filter with.
        """
        if settings.PAGES_USE_SITE_ID:
            if not site_id:
                site_id = settings.SITE_ID
            return self .filter(sites=site_id)
        return self.all()

    def published(self):
        """Return queryset with only published pages"""
        return self.get_query_set().filter(is_published=True, is_hidden=False)
