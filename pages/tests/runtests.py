#!/usr/bin/env python

import os
import sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'test_settings'
test_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, test_dir)

import django
from django.test.runner import DiscoverRunner as TestRunner

django.setup()


def runtests():
    test_runner = TestRunner(verbosity=1, interactive=True, failfast=False)
    failures = test_runner.run_tests(['pages'])
    if os.path.isfile('test.db'):
        os.unlink('test.db')
    return bool(failures)

if __name__ == '__main__':
    sys.exit(runtests())
