
# from django.http import HttpResponse
from django.test import TestCase, RequestFactory
from django.test.utils import override_settings
import os

# A function to be tested
from ..views import is_good_bot

# Good bots (tracable IPs and identifiable user agents)
good_bots_user_agents = [
    ["66.249.79.207", 'Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; Googlebot/2.1; +http://www.google.com/bot.html) Chrome/80.0.3987.92 Safari/537.36'],
    ["40.77.167.144", 'Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)'],
    ['77.88.5.181', 'Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)'],
    ["20.185.79.15", "Mozilla/5.0 (compatible; DuckDuckGo-Favicons-Bot/1.0; +http://duckduckgo.com)"],
    ["17.58.100.38", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/600.2.5 (KHTML, like Gecko) Version/8.0.2 Safari/600.2.5 (Applebot/0.1; +http://www.apple.com/go/applebot)"],
]

# Bad bots (untracable IPs or IPs with mismatched user agents)
bad_bots_user_agents = [
    ["12.249.79.207", 'Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; Googlebot/2.1; +http://www.google.com/bot.html) Chrome/80.0.3987.92 Safari/537.36'],
    ["100.77.167.144", 'Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)'],
    ['122.88.5.181', 'Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)'],
    ["4.208.102.37", "Mozilla/5.0 (compatible; DuckDuckGo-Favicons-Bot/1.0; +http://duckduckgo.com)"],
    ["117.58.100.38", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/600.2.5 (KHTML, like Gecko) Version/8.0.2 Safari/600.2.5 (Applebot/0.1; +http://www.apple.com/go/applebot)"],
]


TEST_TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.dirname(__file__), ],
    },
]

@override_settings(ROOT_URLCONF="friendlybots.tests.urls", TEMPLATES=TEST_TEMPLATES)
class DualViewTests(TestCase):
    """Test the function that loads templates directly from URL router."""

    # good bots must reach the bot_template_name.
    def test_good_bots(self):
        for item in good_bots_user_agents:
            res = self.client.get('/test_dual_view/', REMOTE_ADDR=item[0], HTTP_USER_AGENT=item[1])
            self.assertTrue(b"Hello Friendly Bots" in res.content)

    # bad bots must reach the template_name.
    def test_bad_bots(self):
        for item in bad_bots_user_agents:
            res = self.client.get('/test_dual_view/', REMOTE_ADDR=item[0], HTTP_USER_AGENT=item[1])
            self.assertTrue(b"Hello Enemies" in res.content)


@override_settings(ROOT_URLCONF="friendlybots.tests.urls", TEMPLATES=TEST_TEMPLATES)
class TagBotTests(TestCase):
    """Test the function that loads templates directly from URL router."""

    # template must be rendered for friendly bots.
    def test_good_bots(self):
        for item in good_bots_user_agents:
            res = self.client.get('/test_bot_tag/', REMOTE_ADDR=item[0], HTTP_USER_AGENT=item[1])
            self.assertTrue(b"Hello Friendly Bots" in res.content)

    # template must be rendered for everything that is not a friendly bot.
    def test_bad_bots(self):
        for item in bad_bots_user_agents:
            res = self.client.get('/test_bot_tag/', REMOTE_ADDR=item[0], HTTP_USER_AGENT=item[1])
            self.assertTrue(b"Hello Enemies" in res.content)


@override_settings(ROOT_URLCONF="friendlybots.tests.urls", TEMPLATES=TEST_TEMPLATES)
class AsViewTests(TestCase):
    """Test the function that loads templates directly from URL router."""

    # good bots must reach the template.
    def test_good_bots_template_as_view(self):
        for item in good_bots_user_agents:
            res = self.client.get('/test_as_view/', REMOTE_ADDR=item[0], HTTP_USER_AGENT=item[1])
            self.assertEqual(res.status_code, 200)

    # bad bots must NOT reach the template.
    def test_bad_bots_template_as_view(self):
        for item in bad_bots_user_agents:
            res = self.client.get('/test_as_view/', REMOTE_ADDR=item[0], HTTP_USER_AGENT=item[1])
            self.assertEqual(res.status_code, 403)


@override_settings(ROOT_URLCONF="friendlybots.tests.urls", TEMPLATES=TEST_TEMPLATES)
class DecoratorTests(TestCase):
    """Test the view function decorator."""

    # good bots must reach view function
    def test_good_bot_bypass_decorator(self):
        good_bot_reqs = list()
        for item in good_bots_user_agents:
            res = self.client.get('/test_view_decorator/', REMOTE_ADDR=item[0], HTTP_USER_AGENT=item[1])
            self.assertEqual(res.status_code, 200)

    # bad bots must NOT reach view function
    def test_bad_bot_bypass_decorator(self):
        good_bot_reqs = list()
        for item in bad_bots_user_agents:
            res = self.client.get('/test_view_decorator/', REMOTE_ADDR=item[0], HTTP_USER_AGENT=item[1])
            self.assertEqual(res.status_code, 403)

