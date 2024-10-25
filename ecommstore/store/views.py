from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer 


# View for adding, deleting, and updating a category
@api_view(["GET", "POST", "PUT", "DELETE"])
def category(request):
    category_id = request.GET.get('id')

    # If the category id is not defined return all categories or create a new category
    if not category_id:
        # Handle GET to retreive all categories
        if request.method == 'GET':
            categories = Category.objects.all()
            category_serialized = CategorySerializer(categories, many=True)
            return Response(category_serialized.data, status=status.HTTP_200_OK)
        # Handle POST to create a new category
        elif request.method == 'POST':
            category_serialized = CategorySerializer(data=request.data)
            if category_serialized.is_valid():
                category_serialized.save()
                return Response(category_serialized.data, status=status.HTTP_201_CREATED)
        # If we got this far, the request is invalid
        return Response(category_serialized.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # If the id is defined
    else:
        # retreive the category object by its id
        try:
            category = Category.objects.get(pk=category_id)
        except Category.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        # Handle GET to retreive the category by its id
        if request.method == 'GET':
            category_serialized = CategorySerializer(category)
            return Response(category_serialized.data, status=status.HTTP_200_OK)
        
        # Handle PUT to update the category by its id
        elif request.method == 'PUT':
            category_serialized = CategorySerializer(category, data=request.data)
            if category_serialized.is_valid():
                category_serialized.save()
                return Response(category_serialized.data, status=status.HTTP_200_OK)
            return Response(category_serialized.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # Handle DELETE to delete the category by its id
        elif request.method == 'DELETE':
            category.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    # If nothing is returned so far, it is a bad request that we dont' know how to handle    
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

# View for retriving, updating and deleting a product through its id
# Furthermore, if a pk is not provided, the view will search for a product by name
@api_view(["GET", "POST", "PUT", "DELETE"])
def product(request):
    
    product_id = request.GET.get('id')
    search_term = request.GET.get('search_term')

    # When no query parameters are specified, return all products or create a new product
    if not product_id and not search_term:

        # retreive all products
        if request.method == "GET":
            products = Product.objects.all()
            product_serialized = ProductSerializer(products, many=True)
            return Response(product_serialized.data)
        
        # Handle post to create a new product
        elif request.method == "POST":
            product_serialized = ProductSerializer(data=request.data)
            if product_serialized.is_valid():
                product_serialized.save()
                return Response(product_serialized.data, status=status.HTTP_201_CREATED)
            return Response(product_serialized.errors, status=status.HTTP_400_BAD_REQUEST)
        
    product = None
    # if product_id is defined, retreive the product by its id    
    if product_id:

        try:
            product = Product.objects.get(pk=product_id)
         #   product_serialized = ProductSerializer(product)

        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    # if search_term is defined, search for a product by its name
    if search_term:
        products = Product.objects.filter(name__icontains=search_term)
        product_serialized = ProductSerializer(products, many=True)
        return Response(product_serialized.data, status=status.HTTP_200_OK)
    
    if product:

        if request.method == 'GET':
            product_serialized = ProductSerializer(product)
            return Response(product_serialized.data, status=status.HTTP_200_OK)
        
        # Hanndle PUT to update the product by its id
        elif request.method == 'PUT':
            product_serialized = ProductSerializer(product, data=request.data)
            if product_serialized.is_valid():
                product_serialized.save()
                return Response(product_serialized.data, status=status.HTTP_200_OK)
            
            return Response(product_serialized.errors, status=status.HTTP_400_BAD_REQUEST)
        
        elif request.method == 'DELETE':
            product.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
    
    return Response(status=status.HTTP_400_BAD_REQUEST)
    