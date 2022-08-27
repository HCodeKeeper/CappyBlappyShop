from django.urls import include, path

from . import views

urlpatterns = [
    path('item/add/', views.add_to_cart, name='api_add_item'),
    path('item/remove/', views.remove_from_cart, name='api_remove_item'),
]
