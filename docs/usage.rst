Usage
=====

Start the development server and visit http://127.0.0.1:8000/admin/ to setup
content management system settings (you'll need the Admin app enabled).

Visit http://127.0.0.1:8000/ to use content management system.

Configuration
=============

You must add these apps to your list of ``INSTALLED_APPS`` in ``settings.py``::

    INSTALLED_APPS = (
        ...
        'guardian',
        'mptt',
        'markitup',
        'easy_thumbnails',
        'image_cropping',
        'pages',
    )

Include content management system URLconf in your project urls.py like this::

    urlpatterns = patterns(
    '',
        ...
        url(r'^page/', include('pages.urls')),
    )

Run ``python manage.py syncdb``.  This creates the appropriate tables in your database
that are necessary for operation.

Database migration
------------------

If you use Django 1.5+ you can use database migration by add South application to your django settings.
Django 1.7+ has native database migration support.

Multilingual support
--------------------

All messages and text strings translatable with standard Django i18n framework.
You may use multilingual content for your pages. Default language is English.

Customizing content management system
-------------------------------------

You have a lot of options available to you to customize ``django-pages-cms``.
These options should be defined in your ``settings.py`` file.

**CMS general settings**

* ``PAGES_DEFAULT_LANGUAGE``: default translation language
* ``PAGES_FALLBACK_LANGUAGE``: fallback translation language

* ``PAGES_ALLOW_DJANGO_TEMPLATES``: allow use Django template tags

* ``PAGES_USE_SITE_ID``: use site id application

* ``PAGES_HIDE_SITES``: hide sites django application settings in admin panel

* ``PAGES_DEFAULT_TEMPLATE``: default page template

* ``PAGES_RAISE_403``: raise 403 HTTP ERROR for pages with restricted access
* ``PAGES_RENDER_403``: render 403 HTTP ERROR page for pages with restricted access
* ``PAGES_TEMPLATE_403``: template for 403 HTTP ERROR page

* ``PAGES_PAGE_SLUG_NAME``: slug name used in urls.py

**CMS caching settings**

* ``PAGES_CACHE_BACKEND``: cache backend for pages
* ``PAGES_CACHE_PREFIX``: cache prefix for pages
* ``PAGES_CACHE_DELETE``: delete cache objects for deleted pages
* ``PAGES_PAGE_CACHE_KEY``: cache key for page
* ``PAGES_PAGE_VERSION_KEY``: cache version key for page
* ``PAGES_PAGE_CACHE_TIMEOUT``: default page cache timeout

* ``PAGES_PAGE_HTTP_MAX_AGE``: default page http max age

**CMS image type settings**

* ``PAGES_IMAGE_DIR``: directory for images
* ``PAGES_IMAGE_WIDTH_MAX``: maximum width for images
* ``PAGES_IMAGE_HEIGHT_MAX``: maximum height for images
* ``PAGES_DELETE_IMAGE_FILE``: delete image file for deleted image objects

**CMS extended content types settings**

* ``PAGES_PAGE_EXT_CONTENT_TYPES``: python file with extended content types
* ``PAGES_PAGE_EXT_CONTENT_INLINES``: python file with extended content types inlines for admin panel