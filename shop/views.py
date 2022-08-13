from django.http import HttpResponse
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
    context = {
        "products": product_service.get_products(name)
    }

    return render(request, "catalogue.html", context)
