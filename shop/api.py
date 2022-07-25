from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from helpers.ajax import is_ajax
from services.category_service import *


def categories(request):
    if not is_ajax(request):
        return HttpResponseBadRequest('Invalid request')
    else:
        if request.method == 'GET':
            return JsonResponse(get_categories("/search/"))
        return JsonResponse({'status': 'Invalid request'}, status=400)
