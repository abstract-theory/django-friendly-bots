=====================
Django-Friendly-Bots
=====================

Overview
------------------------
**Django-Friendly-Bots** is a reusable Django app that limits view function access to approved and verified search crawlers. Currently, the approved search engine crawlers are:

.. code-block:: sh

    Google
    Bing
    Yandex
    DuckDuckGo
    AppleBot
    Seznam

Search crawlers are approved by being listed in the code. They are verified using one of the two following methods:

1. Having a white-listed IP address.
2. Reverse DNS look-up of IP, followed by a forwards DNS look-up of resultant hostname, and then having the resultant IP address match the original IP address. For more info search on "verify googlebot".

Notes of bots
-----------------------
For notes on various bots that are of relavance and interest to web developers, see this blog post:

https://abstract-theory.github.io/notes-on-web-crawlers-for-2020.html


Requirements
------------------------
I've tested this on Django version 3.0+. I expect it to run on earlier versions.

Installation
------------------------
It is probably easiest to just drop the source folder into your Django project as you would any other Django app. Django app. Because Django-Friendly-Bots behaves more like a library, it does not need to be added to INSTALLED_APPS. For completeness, the package installation instructions are written below.

to build:

.. code-block:: sh

    python3 /path/setup.py sdist

to install:

.. code-block:: sh

    pip3 install --user /path/django-friendly-bots-1.0.tar.gz

to unistall:

.. code-block:: sh

    pip3 uninstall django-friendly-bots


Setup
---------
Django-Friendly-Bots uses Django's caching suite to store IP addresses and whether or not the IP is a good or bad bot. To use this library, you must have a caching back-end named "friendly_ips" in "settings.py". An example of this is shown below.

.. code-block:: python

    # settings.py
    CACHES = {
        ...
        'friendly_ips': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            'OPTIONS': {
                'MAX_ENTRIES': 500
            }
        }
    }


The view function decorator
---------------------------
This decorator will cause a status code of **403** to be returned to clients if the client is not an approved and verified search engine crawler. The decorator is placed above view functions as shown below.

.. code-block:: python

    from friendlybots.views import search_bots_only

    @search_bots_only()
    def view(request):
        # do something


Testing
-------------------
To run the built-in dev tests using Django's test framework, run

.. code-block:: bash

    python3 manage.py test friendlybots


Caveats
-------------------
It is possible for unapproved crawlers that are owned by companies that also own an approved crawler, to acquire access to restricted HTTP resources. For example, if Google decides to run some specialized crawler that is not explicitly approved, it might pass the credentials check if it operates under the same hostname (google.com). Also, the validity of bot verification is wholly dependent on the companies that run the bots. For example, DuckDuckGo, could add additional IP addresses, or Bing could move hosts from search.msn.com to bing.com.

