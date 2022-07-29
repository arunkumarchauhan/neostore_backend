from django.db import models
from util.models import TimeStampModel
# Create your models here.


class Cart(TimeStampModel):
    user = models.ForeignKey(
        to='user.User', on_delete=models.CASCADE, null=False, blank=False)
    bought = models.BooleanField(default=False)

    class Meta:
        db_table = 'cart'


class CartItem(TimeStampModel):
    product = models.ForeignKey(
        to='product.Product', on_delete=models.CASCADE, null=False, blank=False)
    quantity = models.IntegerField(null=False, blank=False, default=0)
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, null=True, blank=False, related_name='cart_items')

    class Meta:
        db_table = 'cart_item'
