from django.urls import include, path
from rest_framework.routers import SimpleRouter
from .views import CatalogueViewSet
router = SimpleRouter()
router.register(r'products', CatalogueViewSet)
urlpatterns = router.urls
