import django
if django.VERSION[0] >= 2:
    from django.urls import re_path as version_url_path
else:
    from django.conf.urls import url as version_url_path


from ..views import FriendlyBotsView
from .views import view_search_bots_only

urlpatterns = [
    version_url_path(r'^test_as_view/$', FriendlyBotsView.as_view(template_name='hello-friendly-bots.html')),
    version_url_path(r'^test_view_decorator/$', view_search_bots_only),
]
