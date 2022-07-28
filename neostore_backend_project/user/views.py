import email
from functools import partial
from xmlrpc.client import DateTime
from django.http import BadHeaderError
from django.shortcuts import render
from django.urls import path, include
from rest_framework import serializers, viewsets, mixins, status
from rest_framework.response import Response
from user.serializers import FetchUserSeraializer
from user.models import User

from user.serializers import UserSerializer, UpdateAccountSerializer
from .forms import ChangePasswordForm, ForgotForm, LoginForm, UpdateAccountForm, UserRegisterForm
from user.serializers import UserCreateSerializer
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication
from util.helper.functions import generate_password
from django.core.mail import send_mail
import neostore_backend_project.settings as settings


class RegisterView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTTokenUserAuthentication]

    def post(self, request):
        try:
            serializer = UserCreateSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            user = serializer.save()

            refresh = RefreshToken.for_user(user)

            data = UserSerializer(instance=user).data
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "data": data,
                "message": "User Registered Successfully",
                "user_msg": "User Registered Successfully"

            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"message": str(e.args), "user_msg": "Something Went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LoginView(APIView):
    permission_classes = []
    authentication_classes = []

    def post(self, request):
        try:

            login_form = LoginForm(data=request.data)
            if not login_form.is_valid():
                return Response(login_form.errors, status=status.HTTP_400_BAD_REQUEST)
            user = None
            try:
                user = User.objects.get(
                    email=login_form.cleaned_data.get("email", None))
            except User.DoesNotExist:
                return Response({
                    "message": "User Does not Exist",
                    "user_msg": "User does not exist"
                }, status=status.HTTP_404_NOT_FOUND)

            is_password_same = user.check_password(
                raw_password=login_form.cleaned_data.get("password", None))
            if not is_password_same:
                return Response({"message": "Incorrect Password", "user_msg": "Incorrect Password"})

            refresh = RefreshToken.for_user(user)

            data = UserSerializer(instance=user).data
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "data": data,
                "message": "Loggged In Successfully",
                "user_msg": "Logged In Successfully"

            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"message": str(e.args), "user_msg": "Something Went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CheckView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTTokenUserAuthentication]

    def post(self, request):
        print(request.user.id)
        return Response({"message": "user Authenticated"}, status=status.HTTP_200_OK)


class ForgotPasswordView(APIView):
    permission_classes = []
    authentication_classes = []

    def post(self, request):

        try:
            login_form = ForgotForm(data=request.data)

            if not login_form.is_valid():
                return Response(login_form.errors, status=status.HTTP_400_BAD_REQUEST)
            email = login_form.cleaned_data.get("email", None)
            user = None
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({"message": "Invalid User", "user_msg": "Invalid User"}, status=status.HTTP_400_BAD_REQUEST)
            password = generate_password(5)
            user.set_password(password)
            user.confirm_password = password

            try:
                user.email_user('New Password ',
                                'Your new password is : '+password,
                                settings.EMAIL_HOST_USER,
                                [user.email],
                                fail_silently=False,)

                user.save()
            except BadHeaderError:
                return Response({"message": "Wrong Email", "user_msg": "Wrong Email"})
            return Response({"message": "New Password is sent to your email", "user_msg": "New Password is sent to your email"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": "Something went wrong", "user_msg": "Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTTokenUserAuthentication]

    def post(self, request):
        form = ChangePasswordForm(data=request.data)
        if not form.is_valid():
            return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
        try:
            old_password = form.cleaned_data.get("old_password", None)
            password = form.cleaned_data.get("password", None)
            confirm_password = form.cleaned_data.get("confirm_password", None)
            if not password == confirm_password:
                return Response({"message": "Passwords and confirm password do not match", "user_msg": "Passwords and confirm password do not match"}, status=status.HTTP_400_BAD_REQUEST)
            user = User.objects.get(id=request.user.id)
            if user.check_password(old_password):
                user.set_password(password)
                user.save()
                return Response({"message": "Password Updated Successfully", "user_msg": "Password Updated Successfully"}, status=status.HTTP_200_OK)

            else:
                return Response({"message": "Invalid Old Password", "user_msg": "Invalid Old Password"}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"message": "Something went wrong", "user_msg": "Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AccountUpdateView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTTokenUserAuthentication]

    def post(self, request):
        try:
            instance = User.objects.get(id=request.user.id)
            update_serializer = UpdateAccountSerializer(instance=instance,
                                                        data=request.data, partial=True)
            if not update_serializer.is_valid():
                return Response(update_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            update_serializer.save()
            data = UserSerializer(
                instance=User.objects.get(id=request.user.id)).data
            return Response({
                "data": data,
                "message": "Account details updated Successfully",
                "user_msg": "Account details updated Successfully"

            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"message": str(e.args), "user_msg": "Something Went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class FetchAccountDetailView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTTokenUserAuthentication]

    def get(self, request):
        try:
            user = User.objects.get(id=request.user.id)

            return Response(FetchUserSeraializer(instance=user).data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"message": str(e.args), "user_msg": "Something Went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
