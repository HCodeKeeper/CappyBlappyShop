from shop.models import Product
from django.http import JsonResponse


def get_products(quantity):
    products = Product.objects.all()
    if len(products) > quantity:
        products = products[0:quantity]
    return products


class Catalogue:

    @staticmethod
    def get_some_products() -> JsonResponse:
        products = get_products(quantity=20)
        return products


