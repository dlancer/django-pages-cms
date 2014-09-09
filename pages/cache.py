import django

from pages.conf import settings

if django.VERSION[:2] >= (1, 7):
    from django.core.cache import caches
    cache = caches[settings.PAGES_CACHE_BACKEND]
else:
    from django.core import cache as cache_module
    cache = cache_module.get_cache(settings.PAGES_CACHE_BACKEND)
