#!/usr/bin/env python

import os
import sys


def runtests(*test_args):
    if not test_args:
        test_args = ['pages.tests']

    os.environ['DJANGO_SETTINGS_MODULE'] = 'pages.tests.test_settings'
    parent = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, parent)
    import django
    django.setup()

    from django.test.runner import DiscoverRunner as TestRunner
    test_runner = TestRunner(verbosity=1, interactive=True, failfast=False)
    failures = test_runner.run_tests(test_args)
    if os.path.isfile('test.db'):
        os.unlink('test.db')
    sys.exit(failures)


if __name__ == '__main__':
    runtests()
