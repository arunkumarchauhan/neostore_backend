from pyexpat import model
from unicodedata import name
from django.db import models
from neostore_backend_project.settings import MEDIA_URL

from util.models import TimeStampModel
# Create your models here.
import datetime


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


def upload_to(instance, filename):
    file_name = str(datetime.datetime.now())+filename

    return 'images/products/{file_name}'.format(file_name=file_name)


class ProductImages(TimeStampModel):
    product = models.ForeignKey(
        to=Product, on_delete=models.CASCADE, related_name='product_images')
    image = models.ImageField(upload_to=upload_to, null=False, blank=False)

    def get_image(self):
        return MEDIA_URL+self.image.url

    class Meta:
        db_table = 'product_image'
