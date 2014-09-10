#!/usr/bin/env python

import os
import sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'test_settings'
test_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, test_dir)

import django
if django.get_version() >= '1.7':
    django.setup()

if django.get_version() < '1.6':
    from django.test.simple import DjangoTestSuiteRunner as TestRunner
else:
    from django.test.runner import DiscoverRunner as TestRunner


def runtests():
    test_runner = TestRunner(verbosity=1, interactive=True, failfast=False)
    failures = test_runner.run_tests(['pages'])
    if os.path.isfile('test.db'):
        os.unlink('test.db')
    return bool(failures)

if __name__ == '__main__':
    sys.exit(runtests())
