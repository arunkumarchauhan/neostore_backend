# Generated by Django 4.0.6 on 2022-07-29 08:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('address', '0001_initial'),
        ('cart', '0008_alter_cartitem_cart'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('order', '0002_alter_order_table_alter_ordercartmapper_table'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='address',
            field=models.ForeignKey(default=21, on_delete=django.db.models.deletion.CASCADE, to='address.address'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='cart',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='cart.cart'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='user',
            field=models.ForeignKey(default=3, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
