# Generated by Django 4.0.6 on 2022-07-24 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.CharField(max_length=1024),
        ),
        migrations.AlterModelTable(
            name='product',
            table='product',
        ),
        migrations.AlterModelTable(
            name='productcategory',
            table='product_category',
        ),
        migrations.AlterModelTable(
            name='productimages',
            table='product_image',
        ),
    ]
