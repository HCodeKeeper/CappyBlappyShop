from django.urls import include, path
from django.contrib import admin


urlpatterns = [
    path(r'api/', include('shop.urls')),
    path(r'api/auth/', include('authentication.urls')),
    path(r'api/account/', include('accounts.urls')),
    path('api/', include('cart.urls')),
    path('api/checkout/', include('checkout.urls')),
    path('api/event/', include('events.urls')),
    path('api/admin/', admin.site.urls),
]
