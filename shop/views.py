from .models import Product
from django.shortcuts import render
from services import product_service, cart_service, deal_service
from shop.api import *
from rest_framework import viewsets
from rest_framework.response import Response
from .serializers import ProductPreviewSerializer, ProductCompoundSerializer
from .models import Product


def index(request):
    products = product_service.Catalogue.get_some_random_products()
    product_service.insert_discount_in_products(products)
    context = {
        "products": products
    }
    return render(request, "index.html", context)


class CatalogueViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductPreviewSerializer



def catalogue(request):
    name = request.GET.get('product', '')
    page_num = int(request.GET.get('page', '1'))
    try:
        products = product_service.get_products_page(name, page_num)
        product_service.insert_discount_in_products(products.object_list)
        context = {
            "products": products,
            "page_num": page_num,
            "query": name
        }
        return render(request, "catalogue.html", context)
    except IndexError:
        return HttpResponseBadRequest('This page doesn\'t exist')


def product(request, product_id):
    cart_service.Cart(request.session)
    try:
        product_context = product_service.get_product_context(product_id)
        _product = product_context.get_product()
        context = {
            "product": _product,
            "addons": product_context.get_addons(),
            "discounted_price": deal_service.get_discounted_price(_product)
        }
        return render(request, "product.html", context)
    except Product.DoesNotExist:
        return HttpResponseBadRequest('This product doesn\'t exist')


class ProductPageViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductCompoundSerializer
