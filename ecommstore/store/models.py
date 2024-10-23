from django.db import models

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()

class Category(models.Model):
    name = models.CharField(max_length=255)
    products = models.ManyToManyField(Product)