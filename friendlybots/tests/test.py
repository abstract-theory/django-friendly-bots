
from django.http import HttpResponse
from django.test import TestCase, RequestFactory
from ..views import search_bots_only, is_good_bot

# A view function that can only be viewed by approved and verified search engines.
@search_bots_only()
def view_search_bots_only(request):
    return HttpResponse(status=200)


class FriendlyBotTests(TestCase):

    # Good bots (tracable IPs and identifiable user agents)
    good_bots_user_agents = [
        ["66.249.79.207", 'Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; Googlebot/2.1; +http://www.google.com/bot.html) Chrome/80.0.3987.92 Safari/537.36'],
        ["40.77.167.144", 'Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)'],
        ['77.88.5.181', 'Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)'],
        ["54.208.102.37", "Mozilla/5.0 (compatible; DuckDuckGo-Favicons-Bot/1.0; +http://duckduckgo.com)"],
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


    # good bots must NOT show up in the event log.
    def test_good_bot_bypass_lambda(self):
        # test data on function
        for remote_ip, user_agent in self.good_bots_user_agents:
            assert(is_good_bot(remote_ip, user_agent) == True)


    # fake bots must show up in the event log.
    def test_bad_bot_event_lambda(self):
        # test data on function
        for remote_ip, user_agent in self.bad_bots_user_agents:
            assert(is_good_bot(remote_ip, user_agent) == False)



    # good bots must NOT show up in the event log.
    def test_good_bot_bypass_decorator(self):

        # request factory with good bots
        good_bot_reqs = list()
        for item in self.good_bots_user_agents:
            _rf = RequestFactory()
            _req = _rf.get('/fake/url', REMOTE_ADDR=item[0], HTTP_USER_AGENT=item[1])
            good_bot_reqs.append(_req)

        # test requests on view function
        for b_req in good_bot_reqs:
            res = view_search_bots_only(b_req)
            self.assertEqual(res.status_code, 200)


    # fake bots must show up in the event log.
    def test_bad_bot_bypass_decorator(self):

        # request factory with bad bots
        bad_bot_reqs = list()
        for item in self.bad_bots_user_agents:
            _rf = RequestFactory()
            _req = _rf.get('/fake/url', REMOTE_ADDR=item[0], HTTP_USER_AGENT=item[1])
            bad_bot_reqs.append(_req)

        # test requests on view function
        for b_req in bad_bot_reqs:
            res = view_search_bots_only(b_req)
            self.assertEqual(res.status_code, 403)


