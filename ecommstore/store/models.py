from django.db import models

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()

class Category(models.Model):
    name = models.CharField(max_length=255)
    products = models.ManyToManyField(Product)

class Order(models.Model):
    order_id = models.CharField(max_length=255)
    amount = models.IntegerField()
    payment_status = models.BooleanField(default=False)
    payment_id = models.CharField(max_length=255, null=True)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
