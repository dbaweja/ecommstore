from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.product, name='products'),
    path('categories/', views.category, name='categories'),
    path('productsall/', views.ProductViewSet.as_view(), name='productsall'),
    path('orders/', views.CreateOrderView.as_view(), name='create_order'),
]