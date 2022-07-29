

# Create your views here.
from functools import partial
from turtle import update
from rest_framework.views import APIView
from cart.serializers import CartItemSerializer
from cart.forms import ChangeProductQuantityForm, AddCartItemForm
from cart.serializers import GetCartSerializer, CartItemListSerializer
from user.models import User
from .models import *
from rest_framework import generics
from product.models import Product
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication

from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers, viewsets, mixins, status

from rest_framework.response import Response
from django.db.models import Count, F, Value


class AddToCartView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTTokenUserAuthentication]

    def post(self, request):
        try:
            serializer = CartItemSerializer(data=request.data)

            cart = None
            user = None
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            try:
                user = User.objects.get(id=request.user.id)
                cart = Cart.objects.get(user=user, bought=False)

            except Cart.DoesNotExist:
                cart = Cart(user=user)
                cart.save()
            product_id = serializer.validated_data.get(
                'product')
            product_in_cart_query = CartItem.objects.filter(
                product_id=product_id, cart__user_id=request.user.id, cart__bought=False)
            # If adding product is alredy in cart
            if product_in_cart_query.exists():
                last_item_in_cart = product_in_cart_query.last()
                last_item_in_cart.cart = cart
                last_item_in_cart.quantity = last_item_in_cart.quantity+1
                last_item_in_cart.save(update_fields=['quantity', 'cart'])
                serializer = CartItemSerializer(instance=last_item_in_cart)
            else:
                serializer.save(cart=cart)

            return Response({
                "cart_item": serializer.data,
                "message": "Item Added to cart Successfully",
                "user_msg": "Item Added to cart Successfully"
            }, status=status.HTTP_200_OK)
        except Exception as e:
            print(str(e))
            return Response({"message": str(e.args), "user_msg": "Something Went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ChangeProductQuantityView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTTokenUserAuthentication]

    def post(self, request):
        try:
            form = ChangeProductQuantityForm(request.data)

            if not form.is_valid():
                return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
            cart_item_id = form.cleaned_data.get('cart_item_id')
            quantity = form.cleaned_data.get('quantity', 0)

            if quantity == 0:
                item = CartItem.objects.filter(
                    id=cart_item_id, cart__user__id=request.user.id).first()

                if item.cart.user.id == request.user.id:
                    item.delete()
                return Response({"message": "Item Deleted from Cart", "user_msg": "Item Deleted from Cart"}, status=status.HTTP_200_OK)
            cart_item = None
            try:
                cart_item = CartItem.objects.filter(
                    id=cart_item_id, cart__user__id=request.user.id).first()
                cart_item.quantity = quantity

                cart_item.save(update_fields=['quantity'])

            except CartItem.DoesNotExist:
                pass
            return Response(CartItemSerializer(instance=cart_item).data, status=status.HTTP_200_OK)
        except Exception as e:
            print(str(e))
            return Response({"message": str(e.args), "user_msg": "Something Went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DeleteCartItemView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTTokenUserAuthentication]

    def post(self, request):
        try:
            cart_item_id = request.data.get("cart_item_id", None)
            CartItem.objects.filter(
                id=cart_item_id, cart__user__id=request.user.id).delete()

            return Response({"message": "Cart Item deleted", "user_msg": "Cart Item deleted"}, status=status.HTTP_200_OK)
        except Exception as e:
            print(str(e))
            return Response({"message": str(e.args), "user_msg": "Something Went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ListCartItemsView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTTokenUserAuthentication]

    def get(self, request):
        try:
            cart = Cart.objects.filter(
                user__id=request.user.id, bought=False).first()
            if cart == None:
                return Response({"message": "Your cart is empty", "cart_items": [], "cart_id": None}, status=status.HTTP_200_OK)

            carts = GetCartSerializer(instance=cart)

            return Response(carts.data, status=status.HTTP_200_OK)
        except Exception as e:
            print(str(e))
            return Response({"message": str(e.args), "user_msg": "Something Went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
