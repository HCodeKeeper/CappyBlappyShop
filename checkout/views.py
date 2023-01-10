from rest_framework.renderers import JSONRenderer
from .api import create_checkout_session
from rest_framework.response import Response
from rest_framework.decorators import api_view
from services.cart_service import Cart
from django.views.decorators.cache import cache_page

@api_view(['GET'])
def succeed(request):
    cart = Cart(request.session)
    cart.clear()
    return Response({"checkout fulfilled": True})


@api_view(['GET'])
@cache_page(15*60)
def cancel(request):
    return Response({"checkout fulfilled": False})
