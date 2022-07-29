import imp
from os import stat
from django.shortcuts import render
from django.urls import is_valid_path
from address.models import Address
# Create your views here.
from rest_framework.views import APIView
from cart.serializers import GetCartSerializer
from order.serializers import OrderDetailIdSerializer, OrderDetailSerializer
from order.forms import PlaceOrderForm

from order.serializers import OrderCreateSerializer, OrderListSerializer

from .models import *
from rest_framework import generics

from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication

from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers, viewsets, mixins, status

from rest_framework.response import Response
from django.db import transaction


class PlaceOrderView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTTokenUserAuthentication]

    def post(self, request):
        try:

            form = PlaceOrderForm(request.data)
            if not form.is_valid():
                return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
            cart = Cart.objects.filter(
                user_id=request.user.id, bought=False).last()
            if cart == None:
                return Response({"message": "No items in cart to buy", "user_msg": "No items in cart to buy"}, status=status.HTTP_200_OK)
            address_id = form.cleaned_data.get('address_id', None)
            try:
                with transaction.atomic():
                    address = Address.objects.get(
                        id=address_id, user_id=request.user.id)
                    Cart.objects.filter(
                        user_id=request.user.id, bought=False).update(bought=True)
                    cart_serializer = GetCartSerializer(instance=cart)
                    total_amount = cart_serializer.data.get('total_amount')
                    order = Order(cost=total_amount, cart_id=cart.id,
                                  address_id=address.id, user_id=request.user.id)
                    order.save()
                    order_data = OrderCreateSerializer(
                        instance=order).data
                    return Response({"order": order_data, "message": "Order Placed Successfully", "user_msg": "Order Placed Successfully"}, status=status.HTTP_201_CREATED)
            except Exception as e:
                print(e)

                return Response({"message": e.args, "user_msg": "Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except Exception as e:
            print(e)
            return Response({"message": "Something went wrong", "user_msg": "Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GetOrdersListView(generics.ListAPIView):
    allowed_methods = ["GET"]
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTTokenUserAuthentication]
    paginate_by = 20
    model = Order
    serializer_class = OrderListSerializer

    def get_queryset(self):
        return Order.objects.filter(user_id=self.request.user.id)


class GetOrderDetailView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTTokenUserAuthentication]

    def get(self, request, order_id):
        try:
            order = None
            try:
                order = Order.objects.get(id=order_id, user_id=request.user.id)
                serializer = OrderDetailSerializer(instance=order)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Order.DoesNotExist:
                return Response({"message": "Invalid Order Id", "user_msg": "Invalid Order Id"}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"message": "Something went wrong", "user_msg": "Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
