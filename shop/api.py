from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from helpers.ajax import process_ajax
from services.category_service import get_categories
from services.deal_service import get_random_json
from services import reviews


# abandoned
@process_ajax
def categories(request):
    get_categories("/search/")


@process_ajax
def random_deal(request):
    return get_random_json()


# abandoned
@process_ajax
def get_reviews(request, product_id, page):
    return reviews.get_reviews(product_id, page)


# abandoned
@process_ajax
def add_review(request, product_id):
    return process_ajax(request, None)
