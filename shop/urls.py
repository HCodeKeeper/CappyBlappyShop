from django.urls import include, path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('random_deal', views.random_deal, name='api_random_deal')
]