from django.urls import include, path
from . import views

urlpatterns = [
    path('edit_profile/perform', views.edit_profile, name="edit_profile"),
    path('edit_profile/', views.get_edit_profile_page, name="get_edit_profile_page"),
    path('', views.account, name="account"),
]
