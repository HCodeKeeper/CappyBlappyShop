from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from helpers.ajax import is_ajax
from services.category_service import get_categories
from services.deal_service import get_random_json


def categories(request):
    if not is_ajax(request):
        return HttpResponseBadRequest('Invalid request')
    else:
        if request.method == 'GET':
            return JsonResponse(get_categories("/search/"))
        return JsonResponse({'status': 'Invalid request'}, status=400)


def random_deal(request):
    if not is_ajax(request):
        return HttpResponseBadRequest('Invalid request')
    else:
        if request.method == 'GET':
            return JsonResponse(get_random_json())
        return JsonResponse({'status': 'Invalid request'}, status=400)
