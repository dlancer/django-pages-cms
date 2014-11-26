"""
Django migrations for pages app

This package does not contain South migrations.  South migrations can be found
in the ``south_migrations`` package.
"""

SOUTH_ERROR_MESSAGE = """\n
For South support, customize the SOUTH_MIGRATION_MODULES setting like so:

    SOUTH_MIGRATION_MODULES = {
        'pages': 'pages.south_migrations',
    }
"""

# Ensure the user is not using Django 1.6 or below with South
try:
    # noinspection PyUnresolvedReferences
    from django.db import migrations
except ImportError:
    from django.core.exceptions import ImproperlyConfigured
    raise ImproperlyConfigured(SOUTH_ERROR_MESSAGE)
