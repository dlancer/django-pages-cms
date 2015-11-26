"""
Django migrations for pages app

This package does not contain South migrations.
"""

SOUTH_ERROR_MESSAGE = """\n
South migrations not supported!
"""

# Ensure the user is not using Django 1.6 or below with South
try:
    # noinspection PyUnresolvedReferences
    from django.db import migrations
except ImportError:
    from django.core.exceptions import ImproperlyConfigured
    raise ImproperlyConfigured(SOUTH_ERROR_MESSAGE)
