from django.http.response import HttpResponse, HttpResponseNotAllowed
from django.http.request import HttpRequest
from services.cart_service import Cart
import json

"""
The API takes vanilla js ajax which is hardly readable and testable 
JS requests' payload look like this: <QueryDict: {'{"product_id": self.product.id, "count": "1", "addon_id": "-1"}': ['']}>
Though while testing json.loads returns JSONDecodeError
"""


def add_to_cart(request: HttpRequest):
    if request.method == 'POST':
        cart = Cart(request)
        data = json.loads(list(request.POST.keys())[0])
        cart.add(data["product_id"], data["count"], data["addon_id"])
        return HttpResponse("200")
    return HttpResponseNotAllowed()


def remove_from_cart(request):
    if request.method == 'POST':
        cart = Cart(request)
        data = json.load(request).get('payload')
        cart.remove_item(data["product_id"])
        return HttpResponse("200")
    return HttpResponseNotAllowed()


def clear_cart(request):
    if request.method == 'POST':
        cart = Cart(request)
        cart.clear()
        return HttpResponse("200")
    return HttpResponseNotAllowed()


def update_multiple_from_cart(request):
    if request.method == 'POST':
        cart = Cart(request)
        data = json.load(request).get('payload')
        data_list = [[entries["self"], entries["count"]] for entries in data.values()]
        cart.update_multiple_count(data_list)
        return HttpResponse("200")
    return HttpResponseNotAllowed()