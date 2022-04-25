import django
if django.VERSION[0] >= 2:
    from django.urls import re_path as version_url_path
else:
    from django.conf.urls import url as version_url_path

from .views import view_search_bots_only
from ..views import FriendlyBots_as_view
from ..views import FriendlyBotsDualView
from ..views import TagFriendlyBotsView

urlpatterns = [
    version_url_path(
        r'^test_view_decorator/$',
        view_search_bots_only
    ),

    version_url_path(
        r'^test_as_view/$',
        FriendlyBots_as_view(
            template_name='hello-friendly-bots.html'
        )
    ),

    version_url_path(
        r'^test_dual_view/$',
        FriendlyBotsDualView.as_view(
            template_name='hello-enemies.html',
            bot_template_name='hello-friendly-bots.html'
        )
    ),
    version_url_path(
        r'^test_bot_tag/$',
        TagFriendlyBotsView.as_view(
            template_name='hello-somebody.html',
        )
    ),
]
