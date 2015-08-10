import django

from mptt.managers import TreeManager, TreeQuerySet

from pages.conf import settings


class PageManager(TreeManager):

    def get_queryset(self, *args, **kwargs):
        """
        Ensures that this manager always returns nodes in tree order.
        """
        if django.VERSION < (1, 7):
            qs = TreeQuerySet(self.model, using=self._db)
        else:
            qs = super(TreeManager, self).get_queryset(*args, **kwargs)

        # Restrict operations to pages on the current site if needed
        if settings.PAGES_HIDE_SITES and settings.PAGES_USE_SITE_ID:
            return qs.order_by(self.tree_id_attr, self.left_attr).filter(sites=settings.SITE_ID)
        else:
            return qs.order_by(self.tree_id_attr, self.left_attr)

    def on_site(self, site_id=None):
        """Return a :class:`QuerySet` of pages that are published on the site
        defined by the ``SITE_ID`` setting.

        :param site_id: specify the id of the site object to filter with.
        """
        if settings.PAGES_USE_SITE_ID:
            if not site_id:
                site_id = settings.SITE_ID
            return self.get_queryset().filter(sites=site_id)
        return self.all()

    def published(self):
        """Return queryset with only published pages"""
        return self.get_queryset().filter(is_published=True, is_hidden=False)
