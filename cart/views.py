from django.shortcuts import render
from services.cart_service import Cart
from .api import *


def cart(request):
    cart_formed_data = Cart(request).get_data()
    context = {
        "items": cart_formed_data["items"],
        "sub_total_price": cart_formed_data["sub_total_price"],
        "items_count": cart_formed_data["items_count"]
    }
    return render(request, "cart.html", context)
