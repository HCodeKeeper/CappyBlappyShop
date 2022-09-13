from django.urls import include, path

from . import views

urlpatterns = [
    path('', views.cart, name='cart'),
    path('item/add/', views.add_to_cart, name='api_add_item'),
    path('item/remove/', views.remove_from_cart, name='api_remove_item'),
    path('clear/', views.clear_cart, name='api_clear_cart'),
]
