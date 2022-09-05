from django.shortcuts import render
from django.http.response import HttpResponse, HttpResponseNotAllowed
from services.cart_service import Cart
from django.core.cache import cache
import json


def cart(request):
    cart_formed_data = Cart(request).get_data()
    context = {
        "items": cart_formed_data["items"],
        "sub_total_price": cart_formed_data["sub_total_price"],
        "items_count": cart_formed_data["items_count"]
    }
    return render(request, "cart.html", context)


def add_to_cart(request):
    if request.method == 'POST':
        cart = Cart(request)
        data = json.load(request).get('payload')
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


def update_multiple_from_cart(request):
    if request.method == 'POST':
        cart = Cart(request)
        data = json.load(request).get('payload')
        data_list = [[entries["self"], entries["count"]] for entries in data.values()]
        cart.update_multiple_count(data_list)
        return HttpResponse("200")
    return HttpResponseNotAllowed()

