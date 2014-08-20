Simple content management system for Django 1.5+
================================================

``django-pages-cms`` is a simple content management system for Django 1.5+

.. image:: https://travis-ci.org/dlancer/django-pages-cms.svg?branch=master
    :target: https://travis-ci.org/dlancer/django-pages-cms/
    :alt: Build status

.. image:: https://pypip.in/version/django-pages-cms/badge.svg
    :target: https://pypi.python.org/pypi/django-pages-cms/
    :alt: Latest PyPI version

.. image:: https://pypip.in/download/django-pages-cms/badge.svg
    :target: https://pypi.python.org/pypi/django-pages-cms/
    :alt: Number of PyPI downloads

.. image:: https://pypip.in/format/django-pages-cms/badge.svg
    :target: https://pypi.python.org/pypi/django-pages-cms/
    :alt: Download format

.. image:: https://pypip.in/license/django-pages-cms/badge.svg
    :target: https://pypi.python.org/pypi/django-pages-cms/
    :alt: License

Requirements
------------

::

    Django>=1.5
    django-mptt==0.6.1
    django-guardian==1.2.4
    django-image-cropping==0.8.2
    django-markitup==2.2.1
    django-taggit==0.12
    easy-thumbnails==2.0.1
    PyYAML==3.11
    Markdown==2.4.1
    South==1.0

Installation
============

Download and install ``django-pages-cms`` using **one** of the following methods:

PIP
---

You can install the latest stable package running this command::

    $ pip install django-pages-cms

Also you can install the development version running this command::

    $ pip install -e git+http://github.com/dlancer/django-pages-cms.git#egg=pages-dev

Setuptools
----------

You can install the latest stable package running::

    $ easy_install django-pages-cms


Configuration
=============

You must add these apps to your list of ``INSTALLED_APPS`` in ``settings.py``::

    INSTALLED_APPS = (
        ...
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

TODO

Usage
=====

Start the development server and visit http://127.0.0.1:8000/admin/ to setup
content management system settings (you'll need the Admin app enabled).

Visit http://127.0.0.1:8000/ to use content management system.


You may find detailed documentation is in the "docs" directory.