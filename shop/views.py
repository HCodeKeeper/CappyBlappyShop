from rest_framework import viewsets
from .serializers import ProductPreviewSerializer, ProductCompoundSerializer
from .models import Product


class CatalogueViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductPreviewSerializer


class ProductPageViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductCompoundSerializer
