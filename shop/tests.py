from django.test import TestCase, Client, TransactionTestCase
from services import product_service as products, deal_service
from .models import Addon, Category, Deal, Product
from copy import copy
from decimal import Decimal


class CatalogueHttp(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_home_response_code(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)

    def test_search_products(self):
        with self.subTest('page 1 specified  in url'):
            response = self.client.get('/find/', {'product': 'j', 'page': '1'})
            self.assertEqual(response.status_code, 200)
        with self.subTest('non-existent page 999 specified  in url'):
            response = self.client.get('/find/', {'product': 'j', 'page': '999'})
            self.assertEqual(response.status_code, 400)
        with self.subTest('without specifying the page'):
            response = self.client.get('/find/', {'product': 'j'})
            self.assertEqual(response.status_code, 200)
        with self.subTest('without specifying the product'):
            response = self.client.get('/find/')
            self.assertEqual(response.status_code, 200)
        with self.subTest('without specifying the product but with page 1'):
            response = self.client.get('/find/', {'page': '1'})
            self.assertEqual(response.status_code, 200)
        with self.subTest('without specifying the product but with non-existent page 999'):
            response = self.client.get('/find/', {'page': '999'})
            self.assertEqual(response.status_code, 400)


class ProductCase(TransactionTestCase):
    def setUp(self) -> None:
        self.category = Category.objects.create(name='capybaras')
        self.product = Product.objects.create(
            name="Gort", image_src="path/to/image.png",
            rating=5, description="desc", manufacturer="Ouncetopia",
            contact_info="+phone_number, info", price=499.99,
            quantity=200, category=self.category
        )
        self.deal = Deal.objects.create(title="50% off", percents=50, product=self.product)
        self.addon = Addon.objects.create(name="Polishing", price=10, product=self.product)

    def test_integration_product_context(self):
        product_id = self.product.id
        product_bundle: products.Context = products.get_product_context(product_id)
        product = product_bundle.get_product()
        deal = product_bundle.get_deal()
        addons = product_bundle.get_addons()
        self.assertIsNotNone(product)
        self.assertIsNotNone(deal)

        self.assertEqual(product, self.product)
        self.assertEqual(deal, self.deal)
        for i, addon in enumerate(addons):
            with self.subTest(i):
                self.assertIsInstance(addon, Addon)
                self.assertEqual(addon, self.addon)

    def test_applying_discount(self):
        full_price = Decimal(500)
        discount_percentage = 50
        expected_price = 250
        discounted_price = deal_service._apply_discount_on_price(full_price, discount_percentage)
        self.assertEqual(discounted_price, expected_price)

    def test_price_with_discount(self):
        deal_service.get_discounted_price(self.product)

    def test_integration_discount_prescription(self):
        product = copy(self.product)
        products.insert_discount_in_products([product])
        self.assertIsNot(product.discounted_price, 0)

