from django.urls import include, path

from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('random_deal/', views.random_deal, name='api_random_deal'),
    path('categories/', views.categories, name='api_categories'),
    path('find/', views.catalogue, name='catalogue'),
    path('product/<int:product_id>/', views.product, name='product'),
    path('reviews/get/product/<int:product_id>/page/<int:page>/', views.get_reviews, name='api_get_reviews'),
    path("reviews/add/product/<int:product_id>/", views.add_review, name='api_add_review')
]
