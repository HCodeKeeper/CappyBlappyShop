from django.urls import include, path
from django.contrib import admin


urlpatterns = [
    path('', include('shop.urls')),
    path('cart/', include('cart.urls')),
    path('checkout/', include('checkout.urls')),
    path('admin/', admin.site.urls),
]
