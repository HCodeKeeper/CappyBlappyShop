from django.urls import reverse
from django.shortcuts import redirect
import stripe
from cappy_blappy_shop.settings import DOMAIN
from helpers.checkout import generate_product_line
from django.http import HttpResponseNotAllowed, HttpResponseServerError


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
            raise e
            return HttpResponseServerError()

        return redirect(checkout_session.url)
    else:
        return HttpResponseNotAllowed()
