import imp
from django.urls import include, path
from .views import *

urlpatterns = [
    path('<int:product_id>', GetProductDetailView.as_view(),
         name='get_product_detail'),

    path('all', GetProductsListView.as_view(), name="get_products_list"),
    path('add', CreateProductView.as_view(), name="add_product"),
    path('category', CreateProductCategoryView.as_view(),
         name="get_product_category"),
    path('rating/update', SetProductRating.as_view(),
         name="update_product_rating"),
    path('image/upload', CreateListProductImagesView.as_view(),
         name="get_add_product_images")



]
