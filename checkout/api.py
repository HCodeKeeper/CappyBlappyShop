from django.urls import reverse
from django.shortcuts import redirect
import stripe
from services.cart_service import Cart
from cappy_blappy_shop.settings import DOMAIN
from helpers.checkout import generate_product_line
from django.http import HttpResponsePermanentRedirect
from rest_framework.decorators import api_view
from rest_framework.status import HTTP_500_INTERNAL_SERVER_ERROR
from rest_framework.response import Response


@api_view(['POST'])
def create_checkout_session(request):
    cart = Cart(request.session)

    if not cart.has_any():
        return redirect(reverse('cart'))
    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=generate_product_line(request),
            mode='payment',
            success_url=DOMAIN + reverse('checkout_succeed'),
            cancel_url=DOMAIN + reverse('checkout_cancelled'),
        )
    except Exception as e:
        raise e
        return Response(status=HTTP_500_INTERNAL_SERVER_ERROR)

    return HttpResponsePermanentRedirect(redirect_to=checkout_session.url)