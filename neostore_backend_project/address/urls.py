import imp
from django.urls import include, path
from .views import *

urlpatterns = [
    path('all', AddressListView.as_view(), name="get_list_address"),
    path('add', AddressCreateView.as_view(), name="get_create_address"),
]
