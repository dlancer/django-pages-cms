"""
Django settings for example_app project.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""

# debug control
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
TEMPLATE_DEBUG = True
CACHE_DEBUG = True
SESSION_DEBUG = True
DEBUG_TOOLBAR = True

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

from django.utils.translation import ugettext_lazy as _

SITE_ID = 1

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/dev/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '!at4)qus9dqcgv8t_#+6%uz-ispry)mhdd#-fcuake0i8hmz16'

ALLOWED_HOSTS = []

# Internationalization
# https://docs.djangoproject.com/en/dev/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LANGUAGES = (
    ('en', _('English')),
    ('ru', _('Russian')),
)


# List of callables that know how to import templates from various sources.
if TEMPLATE_DEBUG:
    TEMPLATE_LOADERS = (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
        'django.template.loaders.eggs.Loader',
    )
else:
    # if debug disabled we use cached template loaders
    TEMPLATE_LOADERS = (
        ('django.template.loaders.cached.Loader', (
            'django.template.loaders.filesystem.Loader',
            'django.template.loaders.app_directories.Loader',
            'django.template.loaders.eggs.Loader',
        )),
    )


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'mptt',
    'guardian',
    'markitup',
    'easy_thumbnails',
    'image_cropping',
    'pages',
    'extpages',
)


MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)


# Templates settings
TEMPLATE_DIRS = tuple([os.path.join(BASE_DIR, app_name, 'templates') for app_name in INSTALLED_APPS])
TEMPLATE_DIRS += tuple([os.path.join(BASE_DIR, 'templates')])

ROOT_URLCONF = 'example_app.urls'

WSGI_APPLICATION = 'example_app.wsgi.application'


# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Absolute filesystem path to the directory that will hold user-uploaded files.
MEDIA_ROOT = os.path.join(BASE_DIR, 'web/media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
MEDIA_URL = '/media/'

# Absolute filesystem path to the directory that will hold user-uploaded files.
STATIC_ROOT = os.path.join(BASE_DIR, 'web/static')

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'

# guardian settings
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',  # this is default
    'guardian.backends.ObjectPermissionBackend',
)

ANONYMOUS_USER_ID = -1


# easy_thumbnails
# save thumbnail images to a sub-directory relative to the source image.
THUMBNAIL_DEBUG = DEBUG
THUMBNAIL_SUBDIR = 'thumbs'
THUMBNAIL_QUALITY = 95

from easy_thumbnails.conf import settings as thumbnail_settings

THUMBNAIL_PROCESSORS = ('image_cropping.thumbnail_processors.crop_corners', ) + thumbnail_settings.THUMBNAIL_PROCESSORS

# image_cropping
IMAGE_CROPPING_THUMB_SIZE = (400, 400)
IMAGE_CROPPING_SIZE_WARNING = True

# MarkItUp settings
MARKITUP_MEDIA_URL = STATIC_URL
MARKITUP_FILTER = ('markdown.markdown', {'safe_mode': False, 'extensions': ['extra', 'meta', 'nl2br']})
MARKITUP_SET = 'markitup/sets/markdown'
MARKITUP_SKIN = 'markitup/skins/simple'
MARKITUP_AUTO_PREVIEW = True


# pages
PAGES_PAGE_USE_EXT_CONTENT_TYPES = True
PAGES_PAGE_EXT_CONTENT_TYPES = ('extpages.models.pagevideocontent', )
