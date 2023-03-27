from django.test import TestCase, Client, TransactionTestCase
from services import product_service as products, deal_service
from .models import Addon, Category, Deal, Product
from copy import copy
from decimal import Decimal
from django.urls import reverse


class ProductContextRecorderMixin:
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


class ConnectionCase(TestCase):

    def setUp(self) -> None:
        self.client = Client()
        self.category = Category.objects.create(name='capybaras')
        self.product = Product.objects.create(
            name="Gort", image_src="path/to/image.png",
            rating=5, description="desc", manufacturer="Ouncetopia",
            contact_info="+phone_number, info", price=499.99,
            quantity=200, category=self.category
        )

    def test_home_template(self):
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, 'index.html')

    def test_home_response_code(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_catalogue_template(self):
        response = self.client.get(reverse('catalogue'))
        self.assertTemplateUsed(response, 'catalogue.html')

    def test_search_page_1(self):
        response = self.client.get(reverse('catalogue'), {'product': 'j', 'page': '1'})
        self.assertEqual(response.status_code, 200)

    def test_search_page_out_of_bounds(self):
        response = self.client.get(reverse('catalogue'), {'product': 'j', 'page': '999'})
        self.assertEqual(response.status_code, 400)

    def test_search_without_page(self):
        response = self.client.get(reverse('catalogue'), {'product': 'j'})
        self.assertEqual(response.status_code, 200)

    def test_search_anything(self):
        response = self.client.get(reverse('catalogue'))
        self.assertEqual(response.status_code, 200)

    def test_search_anything_on_page_1(self):
        response = self.client.get(reverse('catalogue'), {'page': '1'})
        self.assertEqual(response.status_code, 200)

    def test_search_anything_out_of_bounds(self):
        response = self.client.get(reverse('catalogue'), {'page': '999'})
        self.assertEqual(response.status_code, 400)

    def test_product_template(self):
        response = self.client.get(reverse('product', kwargs={'product_id': self.product.id}))
        self.assertTemplateUsed(response, 'product.html')

    def test_product_page(self):
        response = self.client.get(reverse('product', kwargs={'product_id': self.product.id}))
        self.assertEqual(response.status_code, 200)


# Also has integration and unit tests for product service
class ProductCase(ProductContextRecorderMixin, TransactionTestCase):
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

    def test_products_pagination_searching_category(self):
        second_product = Product.objects.create(
            name="Quandale", image_src="path/to/image.png",
            rating=5, description="desc", manufacturer="Ouncetopia",
            contact_info="+phone_number, info", price=499.99,
            quantity=200, category=self.category
        )
        second_product.save()
        items_per_page_num = 1
        page_1 = products.get_products_page(self.category.name, 1, items_per_page_num)
        page_2 = products.get_products_page(self.category.name, 2, items_per_page_num)
        self.assertEqual(page_1.object_list[0], self.product)
        self.assertEqual(page_2.object_list[0], second_product)

    def test_products_pagination_searching_incomplete_name(self):
        second_product = Product.objects.create(
            name="Gort2", image_src="path/to/image.png",
            rating=5, description="desc", manufacturer="Ouncetopia",
            contact_info="+phone_number, info", price=499.99,
            quantity=200, category=self.category
        )
        items_per_page_num = 1
        page_1 = products.get_products_page("Gort", 1, items_per_page_num)
        page_2 = products.get_products_page("Gort", 2, items_per_page_num)
        self.assertEqual(page_1.object_list[0], self.product)
        self.assertEqual(page_2.object_list[0], second_product)

    def test_getting_random_products(self):
        for i in range(6):
            Product.objects.create(
            name="Gort2", image_src="path/to/image.png",
            rating=5, description="desc", manufacturer="Ouncetopia",
            contact_info="+phone_number, info", price=499.99,
            quantity=200, category=self.category
        )
        quantity = 3
        random_products = products.get_random_products(quantity)
        self.assertEqual(len(random_products), 3)
        self.assertIsInstance(random_products[0], Product)

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


# Also has integration and unit tests for deal service
class DealsCase(ProductContextRecorderMixin, TestCase):
    def test_get_random_deal(self):
        deal = deal_service.get_random()
        self.assertIsInstance(deal, Deal)

    def test_deal_to_json(self):
        deal_json_expected = {self.deal.title: f'/product/{self.deal.product.id}'}
        deal_json = deal_service.deal_to_json(self.deal)
        self.assertEqual(deal_json, deal_json_expected)

    def test_random_deal_api_no_ajax(self):
        response = self.client.get(reverse('api_random_deal'))
        self.assertEqual(response.status_code, 400)

    def test_random_deal_api(self):
        headers = {'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'}
        response = self.client.get(reverse('api_random_deal'), **headers)
        self.assertEqual(response.status_code, 200)

    def test_random_non_existent_deal_api(self):
        Deal.objects.filter().delete()
        response = self.client.get(reverse('api_random_deal'))
        self.assertEqual(response.status_code, 400)
