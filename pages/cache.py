from django.core.cache import caches

from pages.conf import settings

cache = caches[settings.PAGES_CACHE_BACKEND]
