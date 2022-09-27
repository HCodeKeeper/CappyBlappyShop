from django.shortcuts import render, redirect
from django.urls import reverse
import stripe
from services.cart_service import Cart
from helpers.checkout import generate_product_line
from django.http import HttpResponseNotAllowed, HttpResponseServerError

stripe.api_key = 'sk_test_51Lla8dIiiWKWuqBmqZjuQ7Y4Y05HW7yPM797SgZcfDpWuNT4NR64KvUWnmZf6656cq1woZaYO05NPNmqDiAvZX8A00OEcPz7fs'

DOMAIN = "http://localhost:8000"

def create_checkout_session(request):
    if request.method == 'POST':
        try:
            checkout_session = stripe.checkout.Session.create(
                line_items=generate_product_line(request),
                mode='payment',
                success_url=DOMAIN + reverse('checkout_succeed'),
                cancel_url=DOMAIN + reverse('checkout_cancelled'),
            )
        except Exception as e:
            print(e)
            return HttpResponseServerError()

        return redirect(checkout_session.url)
    else:
        return HttpResponseNotAllowed()


def succeed(request):
    cart = Cart(request)
    cart.clear()
    return render(request, "checkout_success.html")


def cancel(request):
    return render(request, "checkout_cancellation.html")
