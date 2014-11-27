from django.conf import settings

PAGES_DEFAULT_LANGUAGE = getattr(settings, 'PAGES_DEFAULT_LANGUAGE', 'en')
PAGES_FALLBACK_LANGUAGE = getattr(settings, 'PAGES_FALLBACK_LANGUAGE', 'en')

PAGES_ALLOW_DJANGO_TEMPLATES = getattr(settings, 'PAGES_ALLOW_DJANGO_TEMPLATES', False)

PAGES_USE_SITE_ID = getattr(settings, 'PAGES_USE_SITE_ID', False)
PAGES_HIDE_SITES = getattr(settings, 'PAGES_HIDE_SITES', True)
PAGES_DEFAULT_TEMPLATE = getattr(settings, 'PAGES_DEFAULT_TEMPLATE', 'pages/page.html')
PAGES_RAISE_403 = getattr(settings, 'PAGES_RAISE_403', True)
PAGES_RENDER_403 = getattr(settings, 'PAGES_RENDER_403', False)
PAGES_TEMPLATE_403 = getattr(settings, 'PAGES_TEMPLATE_403', 'pages/403.html')

PAGES_PAGE_SLUG_NAME = getattr(settings, 'PAGES_PAGE_SLUG_NAME', 'slug')
PAGES_CACHE_BACKEND = getattr(settings, 'PAGES_CACHE_BACKEND', 'default')
PAGES_CACHE_PREFIX = getattr(settings, 'PAGES_CACHE_PREFIX', 'pages_')
PAGES_CACHE_DELETE = getattr(settings, 'PAGES_CACHE_DELETE', False)
PAGES_PAGE_CACHE_KEY = getattr(settings, 'PAGES_PAGE_CACHE_KEY', 'page_cache_key_')
PAGES_PAGE_VERSION_KEY = getattr(settings, 'PAGES_PAGE_VERSION_KEY', 'page_version_key_')
PAGES_PAGE_CACHE_TIMEOUT = getattr(settings, 'PAGES_PAGE_CACHE_TIMEOUT', 31536000)  # timeout 1 year by default

PAGES_PAGE_HTTP_MAX_AGE = getattr(settings, 'PAGES_PAGE_CACHE_TIMEOUT', 3600)  # timeout 1 hour by default

PAGES_FILE_LOCATION = getattr(settings, 'PAGES_FILE_LOCATION', settings.MEDIA_ROOT)
PAGES_FILE_UPLOAD_PERMISSIONS = getattr(
    settings, 'PAGES_FILE_UPLOAD_PERMISSIONS', settings.FILE_UPLOAD_PERMISSIONS)

if getattr(settings, 'FILE_UPLOAD_DIRECTORY_PERMISSIONS', False):
    PAGES_FILE_UPLOAD_DIRECTORY_PERMISSIONS = getattr(
        settings, 'PAGES_FILE_UPLOAD_DIRECTORY_PERMISSIONS', settings.FILE_UPLOAD_DIRECTORY_PERMISSIONS)

PAGES_IMAGE_DIR = getattr(settings, 'PAGES_IMAGE_DIR', 'pages')
PAGES_IMAGE_WIDTH_MAX = getattr(settings, 'PAGES_IMAGE_WIDTH_MAX', 600)
PAGES_IMAGE_HEIGHT_MAX = getattr(settings, 'PAGES_IMAGE_HEIGHT_MAX', 800)
PAGES_DELETE_IMAGE_FILE = getattr(settings, 'PAGES_DELETE_IMAGE_FILE', False)

PAGES_PAGE_EXT_CONTENT_TYPES = getattr(settings, 'PAGES_PAGE_EXT_CONTENT_TYPES', None)
PAGES_PAGE_EXT_CONTENT_INLINES = getattr(settings, 'PAGES_PAGE_EXT_CONTENT_INLINES', None)
