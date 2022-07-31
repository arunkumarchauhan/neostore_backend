
from dataclasses import fields
import os
from tkinter import Image
import uuid
from django.conf import settings
from django.forms import ImageField
from rest_framework import serializers, viewsets
from product.models import ProductImages
from product.models import ProductCategory
from django.core.files.base import ContentFile

from product.models import Product
import requests


class GetProductsListSerializer(serializers.ModelSerializer):
    product_image = serializers.SerializerMethodField()

    def get_product_image(self, obj):
        return ProductImages.objects.filter(product_id=obj.id).values_list('image', flat=True).first()

    class Meta:
        model = Product
        fields = [field.name for field in model._meta.fields]
        fields.append('product_image')


class CreateProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = '__all__'


class ProductImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImages
        fields = '__all__'


class ProductImageCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductImages
        fields = ['product', 'image']

    def to_internal_value(self, data):
        if 'image' in data:
            url = data['image']

            response = requests.get(url)
            extension = url.split('.').pop()
            random_name = uuid.uuid4().hex + '.'+extension

            content_file = ContentFile(response.content, name=random_name)
            data['image'] = content_file
        return super(ProductImageCreateSerializer, self).to_internal_value(data)


class ProductImageGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImages
        fields = ['image']


class GetProductsDetailSerializer(serializers.ModelSerializer):
    product_images = serializers.SerializerMethodField()

    def get_product_images(self, obj):
        request = self.context.get('request')

        images_list = ProductImages.objects.filter(
            product_id=obj.id).values_list('image', flat=True)
        # return [request.build_absolute_uri(settings.MEDIA_URL+image_url) for image_url in images_list]
        return images_list

    class Meta:
        model = Product
        fields = [field.name for field in model._meta.fields]
        fields.append('product_images')
