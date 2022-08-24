from .models import Product
from django.shortcuts import render
from services import product_service
from shop.api import *


def index(request):
    context = {
        "products": product_service.Catalogue.get_some_random_products()
    }
    return render(request, "index.html", context)


def catalogue(request):
    name = request.GET.get('product', '')
    page_num = int(request.GET.get('page', '1'))
    try:
        products = product_service.get_products_page(name, page_num)
        context = {
            "products": products,
            "page_num": page_num,
            "query": name
        }
        return render(request, "catalogue.html", context)
    except IndexError:
        return HttpResponseBadRequest('This page doesn\'t exist')


def product(request, product_id):
    try:
        product_context = product_service.get_product_context(product_id)
        context = {
            "product": product_context.get_product(),
            "addons": product_context.get_addons(),
            "deal": product_context.get_deal(),
            "reviews": product_context.get_reviews()
        }
        return render(request, "product.html", context)
    except Product.DoesNotExist:
        return HttpResponseBadRequest('This product doesn\'t exist')
