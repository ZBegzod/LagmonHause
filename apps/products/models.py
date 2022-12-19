from django.db import models
from django.conf import settings


# Create your models here.

class Category(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='category/images')

    def __str__(self):
        return self.title


class Product(models.Model):

    name = models.CharField(max_length=120)
    price = models.FloatField()
    description = models.TextField(null=True, blank=True, default='')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    available_inventory = models.IntegerField()

    STATUS = [

        (True, 'Mavjud'),
        (True, 'Mavjud emas')

    ]

    status = models.BooleanField(choices=STATUS, default=STATUS[1][1])

    def __str__(self):
        return self.name


class ProductImages(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    image = models.ImageField(upload_to='product/images')

    def __str__(self):
        return self.product
