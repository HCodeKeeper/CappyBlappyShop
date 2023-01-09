from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import Product, Deal, Category
from django.core.exceptions import ObjectDoesNotExist


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ['name']


class DiscountSerializer(ModelSerializer):
    class Meta:
        model = Deal
        fields = '__all__'


class ProductPreviewSerializer(ProductSerializer):
    category = SerializerMethodField()
    discount = SerializerMethodField()

    def get_category(self, obj):
        try:
            category = Category.objects.get(id=obj.category_id)
        except ObjectDoesNotExist:
            return None
        return CategorySerializer(category).data

    def get_discount(self, obj):
        try:
            discount = Deal.objects.get(product_id=obj.id)
        except ObjectDoesNotExist:
            return None
        return DiscountSerializer(discount).data

    class Meta(ProductSerializer.Meta):
        fields = ['id', 'name', 'rating', 'manufacturer', 'price', 'image_src', 'category', 'discount']