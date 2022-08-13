from shop.models import Product
from shop.models import Category
from django.http import JsonResponse


def get_random_products(quantity):
    products = Product.objects.all()
    if products.count() > quantity:
        products = products[0:quantity]
    return products


def get_products(name):
    products = Product.objects.filter(name__icontains=name)
    if not products.count():
        products = get_products_by_category_name(name)
    return products


def get_products_by_category_name(name):
    return Product.objects.filter(category__name__icontains=name)


class Catalogue:

    @staticmethod
    def get_some_random_products() -> JsonResponse:
        products = get_random_products(quantity=20)
        return products


