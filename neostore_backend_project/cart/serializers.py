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
    cart_items = CartItemListSerializer(many=True)

    def to_representation(self, instance):
        result = super(GetCartSerializer, self).to_representation(instance)

        result["total_amount"] = sum([item["sub_total"]
                                     for item in result['cart_items']])
        result['total_quantity'] = len(result['cart_items'])
        return result

    class Meta:
        model = Cart
        fields = ['id', 'cart_items']
