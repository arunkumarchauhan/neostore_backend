from pyexpat import model
from unicodedata import name
from django.db import models

from util.models import TimeStampModel

# Create your models here.


class ProductCategory(TimeStampModel):
    name = models.CharField(blank=False, null=False, max_length=50)
    icon_image = models.URLField(blank=False, null=False)

    class Meta:
        db_table = 'product_category'


class Product(TimeStampModel):
    product_category = models.ForeignKey(
        to=ProductCategory, on_delete=models.CASCADE)
    name = models.CharField(blank=False, null=False, max_length=254)
    producer = models.CharField(null=False, blank=False, max_length=254)
    description = models.CharField(null=False, blank=False, max_length=1024)
    cost = models.DecimalField(max_digits=15, default=0.00, decimal_places=2)
    rating = models.DecimalField(max_digits=15, default=0.00, decimal_places=2)
    view_count = models.IntegerField(default=0)

    class Meta:
        db_table = 'product'


class ProductImages(TimeStampModel):
    product = models.ForeignKey(
        to=Product, on_delete=models.CASCADE, related_name='product_images')
    image = models.URLField(blank=False, null=False)

    class Meta:
        db_table = 'product_image'
