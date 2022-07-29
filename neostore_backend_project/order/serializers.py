
from dataclasses import field
from rest_framework import serializers, viewsets

from cart.serializers import GetCartSerializer
from address.serializers import AddressSerializer
from .models import *


class OrderCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        exclude = ['address', 'cart', 'user']


class OrderListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        exclude = ['address', 'cart', 'user']


class OrderDetailSerializer(serializers.ModelSerializer):
    cart = GetCartSerializer()
    address = AddressSerializer()

    class Meta:
        model = Order
        fields = ['id', 'cost', 'cart', 'address']


class OrderDetailIdSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        exclude = ['cost', 'cart', 'address']
