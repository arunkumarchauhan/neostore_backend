from django.core.files.base import ContentFile
from django.core.files.images import ImageFile
from django.core.files import File
from tempfile import NamedTemporaryFile
from urllib.request import urlopen
from django.shortcuts import render
from django.db import transaction

# Create your views here.
from rest_framework.views import APIView
from product.serializers import ProductImageCreateSerializer
from product.serializers import CreateProductCategorySerializer, ProductImagesSerializer, GetProductsDetailSerializer

from product.serializers import GetProductsListSerializer
from .models import *
from rest_framework import generics

from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication

from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers, viewsets, mixins, status

from rest_framework.response import Response


class GetProductsListView(generics.ListAPIView):
    allowed_methods = ["GET"]
    authentication_classes = []
    paginate_by = 20
    model = Product
    queryset = Product.objects.all()
    serializer_class = GetProductsListSerializer


class CreateProductView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTTokenUserAuthentication]

    model = Product
    queryset = Product.objects.all()
    serializer_class = GetProductsListSerializer

    def post(self, request):
        serializer = GetProductsListSerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Saved Successfully"}, status=status.HTTP_201_CREATED)
        return Response({"message": "Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CreateProductCategoryView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTTokenUserAuthentication]

    model = ProductCategory
    queryset = ProductCategory.objects.all()
    serializer_class = CreateProductCategorySerializer


class SetProductRating(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTTokenUserAuthentication]

    def post(self, request):
        try:
            product = Product.objects.get(
                id=request.data.get('product_id', None))
            rating = request.data.get('rating', None)
            if rating:
                product.rating = (product.rating+rating)/2
                product.save()

            return Response(GetProductsListSerializer(instance=product).data, status=status.HTTP_201_CREATED)
        except Product.DoesNotExist:
            return Response({
                "message": "Product Not Found",
                "user_msg": "Product Not Found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"message": str(e.args), "user_msg": "Something Went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CreateListProductImagesView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTTokenUserAuthentication]

    model = ProductImages
    queryset = ProductImages.objects.all()
    serializer_class = ProductImagesSerializer


class GetProductDetailView(APIView):
    permission_classes = []
    authentication_classes = []

    def get(self, request, product_id):
        try:
            print(product_id)
            product = Product.objects.get(id=product_id)
            return Response(GetProductsDetailSerializer(instance=product).data, status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            return Response({"message": "Invalid Product Id", "user_msg": "Invalid Product Id"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message": str(e.args), "user_msg": "Something Went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AddProductsToDBView(APIView):
    permission_classes = []
    authentication_classes = []

    def post(self, request):
        try:
            import requests
            url = "http://staging.php-dev.in:8844/trainingapp/api/products/"
            product_category_id = request.data.get('product_category_id', 0)
            r = requests.get(url+"getList", params={
                'product_category_id': product_category_id,
                'limit': 1000,
                'offset': 0
            })
            for data in r.json()['data']:
                product_serializer = GetProductsListSerializer(data={
                    "product_category": data['product_category_id'],
                    **data
                })
                with transaction.atomic():
                    if product_serializer.is_valid():
                        product_serializer.save()
                        pd = requests.get(url+"getDetail", params={
                            'product_id': data['id']
                        })
                        pd_data = pd.json()['data']['product_images']

                        for pd_data_item in pd_data:
                            product_image_serializer = ProductImageCreateSerializer(data={
                                "product": product_serializer.data.get('id'),
                                "image":  pd_data_item['image']
                            })

                            if product_image_serializer.is_valid():
                                product_image_serializer.save()
                            else:
                                print(product_image_serializer.errors)
                                return Response(product_image_serializer.errors, status=status.HTTP_304_NOT_MODIFIED)

            return Response(r.json(), status=status.HTTP_200_OK)
        except Exception as e:
            print("EXCEPTION")
            print(e)
            return Response({"message": str(e), "user_msg": "Something Went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
