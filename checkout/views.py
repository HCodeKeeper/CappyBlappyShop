from django.shortcuts import render, redirect
from .api import create_checkout_session


def succeed(request):
    return render(request, "checkout_success.html")


def cancel(request):
    return render(request, "checkout_cancellation.html")
