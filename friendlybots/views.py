"""
Routines for validating desirable crawlers.

date: 2020-03-31

Bots allowed by default:

    Googlebot, Bingbot, Msnbot, YandexBot, Seznam, AppleBot,
    DuckDuckBot, DuckDuckBot-Favicons-Bot

Bots that are verifiable, but not enabled by default:

    Pinterestbot

"""

from django.http import HttpResponse
from django.views.generic import TemplateView
from django.core.cache import caches
import socket

CACHE_NAME = 'friendly_bots'

app_cache = caches[CACHE_NAME]


# IPs used by DuckDuckBot
DUCKDUCKBOT_IPS = [
    '20.191.45.212',
    '23.21.227.69',
    '40.88.21.235',
    '50.16.241.113',
    '50.16.241.114',
    '50.16.241.117',
    '50.16.247.234',
    '52.5.190.19',
    '52.204.97.54',
    '54.197.234.188',
    '54.208.100.253',
    '54.208.102.37',
    '107.21.1.8',
]

# Bots with known IP addresses
# Use a set instead of a list if there is a large number of IPs
GOOD_IPS = DUCKDUCKBOT_IPS


# Bot Hostnames
GOOD_BOTS_HOSTNAMES = [
    'googlebot.com',
    'google.com',
    'search.msn.com',
    'yandex.com',
    'yandex.ru',
    'yandex.com',
    'seznam.cz',
    'applebot.apple.com',
    # 'pinterest.com',
    # 'sogou.com',
]

# substring in user agents
UA_BLOCKS_IDS = [
    'Googlebot',
    'bingbot',
    'msnbot',
    # 'Pinterestbot',
]



# substring in user agents
UA_IDS = [
    'YandexBot',
    'SeznamBot',
    'Applebot',
    # 'Sogou web spider',
]



def ip_query(remote_ip):
    """
    Returns true if the forwards IP lookup of the reverse IP lookup
    gives us the remote_ip. As of 2020-04-01, this is the standard
    method for Google and Bing. It also works with Yandex and Seznam,
    and probably AppleBot.

    args
        remote_ip: string giving IP address

    returns
        res: boolean value. True if IP is for bot domain name.
    """

    res = False
    try:
        # reverse DNS lookup
        hostname = socket.gethostbyaddr(remote_ip)[0]
        # hostname must end with one of the strings in GOOD_BOTS_HOSTNAMES
        if any(hostname.endswith(bot) for bot in GOOD_BOTS_HOSTNAMES):
            # forwards DNS lookup
            ip = socket.gethostbyaddr(hostname)[2][0]
            # Both IP addresses must match
            if ip == remote_ip:
                res = True
    except socket.herror:
        pass
    return res


def is_good_bot(remote_ip, user_agent):
    """
    Checks that bot is approved and then verifies bot with reverse and
    forwards DNS lookups.

    args
        remote_ip: IP address
        user_agent: user agent string

    return
        res: True or False
    """
    # return False if this is not a bot/IP that we are watching for
    res = False

    # All bots MUST have a user agent
    if user_agent is not None:

        # Good bots with white listed IPs. This is for bots with fixed
        # IP addresses.
        if remote_ip in GOOD_IPS:
            res = True

        # Good bots with 8-bit IP blocks. Cache only first 3 bytes. This
        # is intended for bots that crawl your site constantly.
        elif any(bot in user_agent for bot in UA_BLOCKS_IDS):
            ipb = remote_ip.split(".")
            ipb_123 = ".".join(ipb[:3])
            res = app_cache.get(ipb_123)
            if res is None:
                res = ip_query(remote_ip)
                app_cache.set(ipb_123, res)

        # Good bots with IP blocks < 8-bits. Cache the entire address.
        # This is intended for bots that are not as busy on your site.
        elif any(bot in user_agent for bot in UA_IDS):
            res = app_cache.get(remote_ip)
            if res is None:
                res = ip_query(remote_ip)
                app_cache.set(remote_ip, res)

    return res


def search_bots_only():
    """
    A view decorator which blocks all requests with the exception of search engines that are bot whitelisted and verified.
    """
    def real_decorator(viewFunc):
        def wrapper(request, *args, **kwargs):
            remote_ip = request.META.get('REMOTE_ADDR')
            user_agent = request.META.get('HTTP_USER_AGENT')
            if is_good_bot(remote_ip, user_agent):
                result = viewFunc(request, *args, **kwargs)
            else:
                result = HttpResponse(status=403)
            return result
        return wrapper
    return real_decorator


def FriendlyBots_as_view(**initkwargs):
    """A function that blocks all requests with the exception of search
    engines that are bot whitelisted and verified. It is to be used in
    place of TemplateView.as_view."""
    return search_bots_only()(TemplateView.as_view(**initkwargs))
