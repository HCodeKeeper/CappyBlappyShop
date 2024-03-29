from django.urls import include, path
from django.contrib import admin


urlpatterns = [
    path('', include('shop.urls')),
    path('auth/', include('authentication.urls')),
    path('account/', include('accounts.urls')),
    path('cart/', include('cart.urls')),
    path('checkout/', include('checkout.urls')),
    path('event/', include('events.urls')),
    path('admin/', admin.site.urls),
]
