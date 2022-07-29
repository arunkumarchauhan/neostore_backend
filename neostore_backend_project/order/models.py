from django.db import models
from cart.models import Cart

from util.models import TimeStampModel

# Create your models here.


class Order(TimeStampModel):
    cost = models.DecimalField(decimal_places=2, default=0, max_digits=20)
    cart = models.OneToOneField(
        Cart, on_delete=models.CASCADE, null=False, blank=False, unique=True)
    address = models.ForeignKey(
        'address.Address', on_delete=models.CASCADE, null=False, blank=False)
    user = models.ForeignKey(
        'user.User', on_delete=models.CASCADE, null=False, blank=False)

    class Meta:
        db_table = 'order'
        unique_together = ("user", "cart")


class OrderCartMapper(TimeStampModel):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, null=False, blank=False)
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, null=False, blank=False)

    class Meta:
        db_table = 'order_cart_mapper'
