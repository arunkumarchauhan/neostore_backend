

from rest_framework import serializers, viewsets

from address.models import Address


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        exclude = ["user"]
