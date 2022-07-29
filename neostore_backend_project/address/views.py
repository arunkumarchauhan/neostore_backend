from django.shortcuts import render

from address.serializers import AddressSerializer
from .models import *
from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication

from rest_framework.permissions import IsAuthenticated

from rest_framework.response import Response


class AddressListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTTokenUserAuthentication]

    model = Address
    serializer_class = AddressSerializer

    def get_queryset(self):
        user = self.request.user

        return Address.objects.filter(user_id=user.id)


class AddressCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTTokenUserAuthentication]

    model = Address
    queryset = Address.objects.all()
    serializer_class = AddressSerializer

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user.id)
