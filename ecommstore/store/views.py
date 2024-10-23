from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer 

@api_view(["GET", "POST"])
def products(request):
    if request.method == "GET":
        products = Product.objects.all()
        product_serialized = ProductSerializer(products, many=True)
        return Response(product_serialized.data)
    
    elif request.method == "POST":
        product_serialized = ProductSerializer(data=request.data)
        if product_serialized.is_valid():
            product_serialized.save()
            return Response(product_serialized.data, status=status.HTTP_201_CREATED)
        
        return Response(product_serialized.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET", "PUT", "DELETE"])
def product(request, key):
    try:
        product = Product.objects.get(pk=key)

    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        product_serialized = ProductSerializer(product)
        return Response(product_serialized.data, status=status.HTTP_200_OK)
    
    elif request.method == 'PUT':
        product_serialized = ProductSerializer(product, data=request.data)

        if product_serialized.is_valid():
            product_serialized.save()
            return Response(product_serialized.data, status=status.HTTP_200_OK)
        
        return Response(product_serialized.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    