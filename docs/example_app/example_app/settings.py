"""
Django settings for example_app project.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from django.utils.translation import ugettext_lazy as _

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

SITE_ID = 1

# debug control
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
CACHE_DEBUG = True
SESSION_DEBUG = True
DEBUG_TOOLBAR = True

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
    'pages',
#    'extpages',
#    'embed_video',
)


MIDDLEWARE = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)


# Templates settings
TPL_DIRS = tuple([os.path.join(BASE_DIR, 'templates')])

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': TPL_DIRS,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.request',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
            ],
            'debug': DEBUG
        },
    },
]

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

# MarkItUp settings
MARKITUP_MEDIA_URL = STATIC_URL
MARKITUP_FILTER = ('markdown.markdown', {'safe_mode': False, 'extensions': ['extra', 'meta', 'nl2br']})
MARKITUP_SET = 'markitup/sets/markdown'
MARKITUP_SKIN = 'markitup/skins/simple'
MARKITUP_AUTO_PREVIEW = True


# pages
PAGES_PAGE_USE_EXT_CONTENT_TYPES = True
PAGES_PAGE_EXT_CONTENT_TYPES = ('extpages.models.pagevideocontent', )
