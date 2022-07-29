from dataclasses import field
from statistics import mode
from xml.dom import ValidationErr
from rest_framework import serializers, viewsets

from product.serializers import GetProductsSerializer
from .models import *
from product.models import Product


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['id', 'user']


class CartItemSerializer(serializers.ModelSerializer):
    def validate_quantity(self, value):
        if value < 1:
            raise serializers.ValidationError("Qunatity Cannot be less than 1")
        return value

    class Meta:
        model = CartItem
        fields = "__all__"


class CartItemListSerializer(serializers.ModelSerializer):
    product = GetProductsSerializer(read_only=True)
    sub_total = serializers.SerializerMethodField()

    def get_sub_total(self, obj):
        return obj.quantity*obj.product.cost

    class Meta:
        model = CartItem
        # get all fields name
        fields = [field.name for field in model._meta.fields]
        # add one custom field
        fields.append('sub_total')


class GetCartSerializer(serializers.ModelSerializer):
    cart = CartItemListSerializer()

    class Meta:
        model = Cart
        fields = ['id', 'cart']
