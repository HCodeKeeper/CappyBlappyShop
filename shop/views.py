from django.http import HttpResponse
from django.shortcuts import render
from services import product_service
from shop.api import *


def index(request):
    context = {
        "products": product_service.Catalogue.get_some_products()
    }
    return render(request, "index.html", context)


