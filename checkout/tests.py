from django.test import TestCase
from django.urls import reverse
from service_tests import insert_session
from shop.tests import ProductContextRecorderMixin
from django.test import RequestFactory, Client
from .api import create_checkout_session
from .views import succeed
from services.cart_service import Cart


class Results(ProductContextRecorderMixin, TestCase):

    def setUp(self) -> None:
        super().setUp()
        self.request_factory = RequestFactory()
        self.client = Client()

    def _test_cart_data_populated(self, data):
        self._cart_data_checker(data, True)

    def _test_cart_data_empty(self, data):
        self._cart_data_checker(data, False)

    def _cart_data_checker(self, data: dict, expect_populated: bool):
        for _, detail_key in enumerate(data.keys()):
            with self.subTest():
                self.assertEqual(bool(data[detail_key]), expect_populated, data)

    def test_success_connection(self):
        response = self.client.get(reverse('checkout_succeed'))
        self.assertEqual(response.status_code, 200)

    def test_success_template(self):
        response = self.client.get(reverse('checkout_succeed'))
        self.assertTemplateUsed(response, template_name='checkout_success.html')

    def test_success(self):
        request = self.request_factory.get(reverse('checkout_succeed'))
        insert_session(request, succeed)

        cart = Cart(request)
        cart.add(self.product.id, 1, self.addon.id)

        populated_cart_data = cart.get_data()
        self._test_cart_data_populated(populated_cart_data)

        succeed(request)
        updated_cart_data = Cart(request).get_data()
        self._test_cart_data_empty(updated_cart_data)

    def test_cancel_connection(self):
        response = self.client.get(reverse('checkout_cancelled'))
        self.assertEqual(response.status_code, 200)

    def test_cancel_template(self):
        response = self.client.get(reverse('checkout_cancelled'))
        self.assertTemplateUsed(response, 'checkout_cancellation.html')


class Checkout(ProductContextRecorderMixin, TestCase):
    def setUp(self) -> None:
        super(Checkout, self).setUp()
        self.client = Client()
        self.request_factory = RequestFactory()

    def test_success(self):
        request = self.request_factory.post('create_checkout_session')
        insert_session(request, create_checkout_session)

        cart = Cart(request)
        cart.add(self.product.id, 2)

        response = create_checkout_session(request)
        self.assertEqual(response.status_code, 302)
        self.assertIn('stripe', response.url)

    def test_empty_cart(self):
        request = self.request_factory.post('create_checkout_session')
        insert_session(request, create_checkout_session)

        response = create_checkout_session(request)
        self.assertEqual(response.url, reverse('cart'))
