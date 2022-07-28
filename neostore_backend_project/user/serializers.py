from dataclasses import field
from rest_framework import serializers, viewsets

from user.models import User

# Create your views here.
# Serializers define the API representation.


class UserCreateSerializer(serializers.ModelSerializer):
    username = serializers.CharField()

    class Meta:
        model = User
        fields = "__all__"

    def get_username(self):
        return self.first_name+self.last_name

    extra_kwargs = {"password": {"write_only": True},
                    "confirm_password": {"write_only": True}}

    def is_valid(self, raise_exception=False):
        return super().is_valid(raise_exception)

    def create(self, validated_data):
        password = validated_data["password"]
        cnf_password = validated_data["confirm_password"]
        if(password != cnf_password):
            raise serializers.ValidationError(
                "Password and confirm password are not same")
        user = User(**validated_data, username=self.get_username)
        user.set_password(user.password)
        user.confirm_password = user.password
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ["password", "confirm_password", "is_superuser",
                   "is_staff", "groups", "user_permissions"]


class UpdateAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "first_name", "last_name",
                  "dob", "profile_pic", "phone_no"]


class FetchUserSeraializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', "email", "first_name", "last_name", 'last_login', 'country_id',
                  "dob", "profile_pic", "phone_no", 'username', 'is_active', 'created_at', 'modified_at']
