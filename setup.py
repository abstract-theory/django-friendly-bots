import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-friendly-bots',
    version='1.2',
    packages=find_packages(),
    include_package_data=True,
    license='GNU GPLv3',  # example license
    description='A Django app that limits access to only approved and verified crawlers.',
    long_description=("A Django app to limit view function access to only approved and verified crawlers. "
                      "By default, the approved crawlers are: Google, Bing, Msnbot, Yandex, Seznam, AppleBot, and DuckDuckGo. "
                      "All crawlers are verified by either reverse and forwards DNS lookups or by having a white-listed IP address. "
                      "Watch your logs. Crawler verification methods require that crawlers keep doing things in a certain way."),
    long_description=README,
    url='https://github.com/abstract-theory',
    author='',
    author_email='',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.9',
        'Framework :: Django :: 2.0',
        'Framework :: Django :: 2.1',
        'Framework :: Django :: 2.2',
        'Framework :: Django :: 3.0',
        'Framework :: Django :: 4.0',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU GPLv3',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
