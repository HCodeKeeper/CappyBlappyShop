from django.shortcuts import render, redirect
from .api import create_checkout_session
from services.cart_service import Cart


def succeed(request):
    cart = Cart(request)
    cart.clear()
    return render(request, "checkout_success.html")


def cancel(request):
    return render(request, "checkout_cancellation.html")
