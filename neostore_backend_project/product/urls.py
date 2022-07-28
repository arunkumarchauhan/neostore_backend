import imp
from django.urls import include, path
from .views import *

urlpatterns = [
    path('all', GetProductsView.as_view(), name="get_products_list"),
    path('add', CreateProductView.as_view(), name="add_product"),
    path('category', CreateProductCategoryView.as_view(),
         name="get_product_category"),

    path('rating/update', SetProductRating.as_view(),
         name="update_product_rating"),



]
