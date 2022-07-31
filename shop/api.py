from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from helpers.ajax import process_ajax
from services.category_service import get_categories
from services.deal_service import get_random_json


def categories(request):
    return process_ajax(request, get_categories("/search/"))


def random_deal(request):
    return process_ajax(request, get_random_json())
