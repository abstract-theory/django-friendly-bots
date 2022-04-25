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

Notes on bots
-----------------------
For notes on various bots that are of relevance and interest to web developers, see this blog post:

https://abstract-theory.github.io/notes-on-web-crawlers-for-2020.html


Requirements
------------------------
The included tests have been run successfully on the following Django versions: 1.9, 2.0, 3.0, 4.0.


Installation
------------------------
It is probably easiest to just drop the source folder into your Django project as you would any other Django app. For completeness, the package installation instructions are written below.

Django-Friendly-Bots behaves somewhat like a library (rather than a Django app), however, to either run the included tests or use the management command, it needs to be added to INSTALLED_APPS.

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
Django-Friendly-Bots uses Django's caching suite to store IP addresses and whether or not the IP is a good or bad bot. To use this library, you must have a caching back-end named "friendly_bots" in "settings.py". An example of this is shown below.

.. code-block:: python

    # settings.py
    CACHES = {
        ...
        'friendly_bots': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            'OPTIONS': {
                'MAX_ENTRIES': 500
            }
        }
    }


Usage
-----

Protecting View Functions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The decorator, **@search_bots_only()** will cause a status code of **403** to be returned to clients if the client is not an approved and verified search engine crawler. The decorator is placed above view functions as shown below.

.. code-block:: python

    # views.py
    from friendlybots.views import search_bots_only

    @search_bots_only()
    def view(request):
        # do something


Protecting Templates
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The function **FriendlyBots_as_view** can be used in place of TemplateView.as_view. Using **FriendlyBots_as_view** returns regular pages to approved and verified bots **403** for everyone else. Usage of the function is illustrated below.

.. code-block:: python

    # urls.py
    from friendlybots.views import FriendlyBots_as_view

    urlpatterns = [
        re_path(
            r'^test_as_view/$',
            FriendlyBots_as_view(
                template_name='hello-friendly-bots.html'
            )
        ),
    ]

Serving Two Templates from One URL
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The method **FriendlyBotsDualView.as_view** can be used in place of TemplateView.as_view. Using **FriendlyBotsDualView.as_view** will use one of two templates depending on whether or not the requester is an approved and verified bot. Usage of this method is illustrated below.

.. code-block:: python

    # urls.py
    from friendlybots.views import FriendlyBotsDualView

    urlpatterns = [
        re_path(
            r'^hello-friendly-bots/$',
            FriendlyBotsDualView.as_view(
                template_name='hello-enemies.html',
                bot_template_name='hello-friendly-bots.html'
            )
        ),
    ]


Identifying Friendly Bots with a Template Variable
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The method **TagFriendlyBotsView.as_view** can be used in place of TemplateView.as_view. Using **TagFriendlyBotsView.as_view** passes a boolean value to templates that depends on whether or not the requester is an approved and verified bot. Usage of this method is illustrated below.

.. code-block:: python

    # urls.py
    from friendlybots.views import TagFriendlyBotsView

    urlpatterns = [
        re_path(
            r'^hello-friendly-bots/$',
            TagFriendlyBotsView.as_view(
                template_name='hello-somebody.html',
            )
        ),
    ]

.. code-block:: html

    <!-- hello-somebody.html -->
    <html>
        <body>
            {% if is_friendly_bot %}
                <h1>Hello Friendly Bots!</h1>
            {% else %}
                <h1>Hello Scrapers!</h1>
            {% endif %}
        </body>
    </html>


Management Commands
^^^^^^^^^^^^^^^^^^^
If, for any reason, IPs are incorrectly labels as good or bad bots (e.g. a search engine changes IP addresses), the cached IP addresses can be deleted with a management command. This is illustrated below.

.. code-block:: sh

    django-admin friendlybots --clear


Running Builtin Tests
^^^^^^^^^^^^^^^^^^^^^^^
To run the built-in dev tests using Django's test framework, run

.. code-block:: sh

    django-admin test friendlybots


Caveats
-------------------
Currently, FriendlyBots has been designed only for IPv4. It *might* work for IPv6. One thing that comes to mind is that the address space for IPv6 is much bigger. If bots started using massive ranges of IP addresses, this could cause the IP address caching strategy to become ineffective.

It may be possible to acquire access to restricted HTTP resources if a company owning an approved crawler is also running an additional unapproved bot. A bot will pass the credentials check if it both operates under one of the GOOD_BOTS_HOSTNAMES and its user-agent string contains one of the string in either UA_BLOCKS_IDS or UA_IDS.

Also, the validity of bot verification is wholly dependent on the companies that run the bots. For example, Bing could move hosts from search.msn.com to bing.com.

Note: DuckDuckGo has changed their crawler's IP addresses a couple of times recently. Addresses are current as of 2022-04-25. To change IPs, edit the variable "DUCKDUCKBOT_IPS" in "views.py".

