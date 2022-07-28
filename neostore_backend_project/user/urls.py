from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from .views import *

urlpatterns = [
    path('register', RegisterView.as_view(), name="register_"),
    path('login', LoginView.as_view(), name="login_"),
    path('check', CheckView.as_view(), name="check_"),

    path('forgot-password', ForgotPasswordView.as_view(),
         name="forgot_password"),
    path('change-password', ChangePasswordView.as_view(),
         name="change_password"),
    path('update', AccountUpdateView.as_view(),
         name="update_account"),
    path('detail', FetchAccountDetailView.as_view(),
         name="get_account_detail"),




]
