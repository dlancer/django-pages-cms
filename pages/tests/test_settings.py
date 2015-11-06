import os

SITE_ID = 1

BASE_DIR = os.path.dirname(__file__)

from django.utils.translation import ugettext_lazy as _

ROOT_URLCONF = 'urls'
SECRET_KEY = 'secretkey'
SITE_ROOT = os.path.dirname(os.path.abspath(__file__))

LANGUAGE_CODE = 'en'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LANGUAGES = (
    ('en', _('English')),
    ('de', _('German')),
    ('ru', _('Russian')),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.contenttypes',
    'django.contrib.admin',
    'django.contrib.messages',
    'django.contrib.sites',
    'guardian',
    'mptt',
    'markitup',
    'easy_thumbnails',
    'image_cropping',
    'pages',
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'test.db',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware'
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.messages.context_processors.messages',
)

# Templates settings
TEMPLATE_DIRS = tuple([os.path.join(BASE_DIR, app_name, 'templates') for app_name in INSTALLED_APPS])
TEMPLATE_DIRS += tuple([os.path.join(BASE_DIR, 'templates')])


# django-guardian settings
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'guardian.backends.ObjectPermissionBackend',
)

ANONYMOUS_USER_ID = -1

# MarkItUp settings
MARKITUP_FILTER = ('markdown.markdown', {'safe_mode': False, 'extensions': ['extra', 'meta', 'nl2br']})

PAGES_CACHE_DELETE = True
