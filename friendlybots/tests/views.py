from django.http import HttpResponse
from ..views import search_bots_only

@search_bots_only()
def view_search_bots_only(request):
    return HttpResponse(status=200)
