from django.shortcuts import render, redirect
from .api import create_checkout_session
from services.cart_service import Cart
from django.views.decorators.cache import cache_page


def succeed(request):
    cart = Cart(request)
    cart.clear()
    return render(request, "checkout_success.html")


@cache_page(15*60)
def cancel(request):
    return render(request, "checkout_cancellation.html")
