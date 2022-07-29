from django.db import models

# Create your models here.


class Address(models.Model):
    user = models.ForeignKey(
        to='user.User', on_delete=models.CASCADE, null=False, blank=False)
    address = models.CharField(null=False, blank=False, max_length=1024)
    landmark = models.CharField(null=False, blank=False, max_length=254)
    city = models.CharField(null=False, blank=False, max_length=254)
    state = models.CharField(null=False, blank=False, max_length=254)
    zipcode = models.IntegerField(null=False, blank=False)
    country = models.CharField(null=False, blank=False, max_length=254)

    class Meta:
        db_table = 'address'
