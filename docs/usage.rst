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
        'pages',
    )


Include content management system URLconf in your project urls.py like this::

    urlpatterns = i18n_patterns(url(r'^page/', include('pages.urls', namespace='pages')),)

Run ``python manage.py migrate``.
This creates the appropriate tables in your database that are necessary for operation.

After database creation you must load standard content types to database from provided fixtures::

    $ python manage.py loaddata content_types


Database migration
------------------

Django 1.7+ has native database migration support.

Django 1.10+ support
--------------------

Django 1.10+ not supported at the moment

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

* ``PAGES_USE_FALLBACK_LANGUAGE``: use fallback translation language
* ``PAGES_FALLBACK_LANGUAGE``: fallback translation language
* ``FALLBACK_LANGUAGE_COOKIE_NAME``: fallback translation language cookie name

* ``PAGES_ALLOW_DJANGO_TEMPLATES``: allow use Django template tags

* ``PAGES_USE_SITE_ID``: use site id application

* ``PAGES_HIDE_SITES``: hide sites django application settings in admin panel

* ``PAGES_DEFAULT_TEMPLATE``: default page template

* ``PAGES_RAISE_403``: raise 403 HTTP ERROR for pages with restricted access
* ``PAGES_RENDER_403``: render 403 HTTP ERROR page for pages with restricted access
* ``PAGES_TEMPLATE_403``: template for 403 HTTP ERROR page

* ``PAGES_PAGE_SLUG_NAME``: slug name used in urls.py
* ``PAGES_HOME_PAGE_SLUG``: home page slug, for proper redirection to home page

**CMS caching settings**

* ``PAGES_CACHE_BACKEND``: cache backend for pages
* ``PAGES_CACHE_PREFIX``: cache prefix for pages
* ``PAGES_CACHE_DELETE``: delete cache objects for deleted pages
* ``PAGES_PAGE_CACHE_KEY``: cache key for page
* ``PAGES_PAGE_VERSION_KEY``: cache version key for page
* ``PAGES_PAGE_CACHE_TIMEOUT``: default page cache timeout

* ``PAGES_PAGE_HTTP_MAX_AGE``: default page http max age

**CMS extended content types settings**

* ``PAGES_PAGE_USE_EXT_CONTENT_TYPES``: extended content types support
* ``PAGES_PAGE_EXT_CONTENT_TYPES``: extended content types models
* ``PAGES_PAGE_EXT_CONTENT_INLINES``: extended content types inlines for admin panel


Extended content types
======================

Extended content types support is disabled by default. If you want use extended content types
you should setup these options in your Django project settings:

* ``PAGES_PAGE_USE_EXT_CONTENT_TYPES`` = True
* ``PAGES_PAGE_EXT_CONTENT_TYPES`` = list(your extend content types models)
* ``PAGES_PAGE_EXT_CONTENT_INLINES`` = list(your extend content types inlines for admin panel)

You also should add your extended content types to PageContentType table.

You may use embed video content type realisation in example project. You may find it in the docs/example_app directory.
You also can use ``django-pages-cms-extensions`` application as full tutorial.
You can find ``django-pages-cms-extensions`` here: http://github.com/dlancer/django-pages-cms-extensions

Another settings
================

* ``PAGES_PAGE_USE_META_TITLE_FOR_SLUG``: use title from page meta for slug generation (default: True)
* ``PAGES_PAGE_ACTIVE_CSS_CLASS``: css class name for current active page

Add any data to page context
============================

You can add any data to your pages. Just subclass PageDetailsView, override get_context_data method,
and your data will be added to page context before rendering. You can use this for create special pages,
i.e. for add pagination support to your page.

Default content page types
==========================

You can create default page content types objects for faster page creation.
PageDefaultContent object have two fields:

* ``name``: you can use any unique name for your default content set
* ``content_types``: string with all content types you need, separated by colons.

Example:

.. code:: python

  PageDefaultContent.create(
     name = 'page_slug_meta_markdown',
     content_types = 'slug:meta:markdown'
  )
