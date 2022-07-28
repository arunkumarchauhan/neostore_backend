from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from product.serializers import CreateProductCategorySerializer

from product.serializers import GetProductsSerializer
from .models import *
from rest_framework import generics

from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication

from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers, viewsets, mixins, status

from rest_framework.response import Response


class GetProductsView(generics.ListAPIView):
    allowed_methods = ["GET"]
    authentication_classes = []
    paginate_by = 10
    model = Product
    queryset = Product.objects.all()
    serializer_class = GetProductsSerializer


class CreateProductView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTTokenUserAuthentication]

    model = Product
    queryset = Product.objects.all()
    serializer_class = GetProductsSerializer

    def post(self, request):
        serializer = GetProductsSerializer(data=request.data, many=True)
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

            return Response(GetProductsSerializer(instance=product).data, status=status.HTTP_201_CREATED)
        except Product.DoesNotExist:
            return Response({
                "message": "Product Not Found",
                "user_msg": "Product Not Found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"message": str(e.args), "user_msg": "Something Went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
