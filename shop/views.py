from django.http import HttpResponse
from django.shortcuts import render
from api import *

def index(request):
    context = {}
    return render(request, "index.html")


