from shop.models import Product
from django.http import JsonResponse
from django.core.paginator import Paginator


def get_random_products(quantity):
    products = Product.objects.all()
    if products.count() > quantity:
        products = products[0:quantity]
    return products


def get_products_page(name, page_num):
    items_per_page_count = 8
    paginator = Paginator(get_products(name), items_per_page_count)
    if page_num > paginator.num_pages or page_num < 1:
        raise IndexError("page number is above of existing count")
    return paginator.page(page_num)


def get_products(name):
    products = get_products_by_category_name(name)
    if not products.count():
        products = Product.objects.filter(name__icontains=name).order_by("name")
    return products


def get_products_by_category_name(name):
    return Product.objects.filter(category__name__iexact=name).order_by("category__name")


class Catalogue:

    @staticmethod
    def get_some_random_products() -> JsonResponse:
        products = get_random_products(quantity=20)
        return products


