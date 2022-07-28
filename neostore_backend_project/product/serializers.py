
from dataclasses import fields
from rest_framework import serializers, viewsets
from product.models import ProductCategory

from product.models import Product


class GetProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class CreateProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = '__all__'
