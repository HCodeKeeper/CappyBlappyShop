from django.urls import include, path

from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('random_deal/', views.random_deal, name='api_random_deal'),
    path('categories/', views.categories, name='api_categories'),
    path('find/', views.catalogue, name='catalogue'),
    path('product/<int:product_id>/', views.product, name='product'),
]
