

from ast import List
import imp
from django.urls import include, path
from .views import *

urlpatterns = [
    path('add', AddToCartView.as_view(), name="add_to_cart"),
    path('update/quantity', ChangeProductQuantityView.as_view(),
         name="update_quantity"),
    path('delete', DeleteCartItemView.as_view(),
         name="delete_cart_item"),
    path('all', ListCartItemsView.as_view(),
         name="get_cart_item"),



]
