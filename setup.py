import os
from setuptools import setup, find_packages
from pages import get_version as get_package_version


README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()
REQUIREMENTS = os.path.join(os.path.dirname(__file__), 'requirements.txt')
reqs = open(REQUIREMENTS).read().splitlines()


# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

try:
    import importlib
except ImportError:
    reqs.append('importlib')

setup(
    name='django-pages-cms',
    version=get_package_version(),
    packages=find_packages(),
    include_package_data=True,
    install_requires=reqs,
    license='BSD',
    description='Simple content management system for Django 1.7+',
    long_description=README,
    url='https://github.com/dlancer/django-pages-cms',
    author='dlancer',
    author_email='dmdpost@gmail.com',
    maintainer='dlancer',
    maintainer_email='dmdpost@gmail.com',
    zip_safe=False,
    use_2to3=True,
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Development Status :: 3 - Alpha',
    ],)
