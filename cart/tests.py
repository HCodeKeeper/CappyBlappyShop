from django.test import TestCase
from shop.tests import ProductContextRecorderMixin
from django.test.client import Client
from services.cart_service import Cart
from django.test import RequestFactory
from django.urls import reverse
from .views import cart as cart_view
from checkout.tests import insert_session


# AJAX API is hardly testable

class CartCase(ProductContextRecorderMixin, TestCase):
    def setUp(self) -> None:
        super(CartCase, self).setUp()
        self.request_factory = RequestFactory()
        self.client = Client()

    def test_empty_cart(self):
        response = self.client.get(reverse('cart'))
        self.assertEqual(response.status_code, 200)

    def test_cart(self):
        request = self.request_factory.get(reverse('cart'))
        insert_session(request, cart_view)

        cart = Cart(request)
        cart.add(self.product.id, 2)

        response = cart_view(request)
        self.assertEqual(response.status_code, 200)
