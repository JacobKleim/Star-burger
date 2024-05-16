# Generated by Django 3.2.15 on 2024-05-16 13:18

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0041_auto_20240516_1653'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='product_price',
            field=models.DecimalField(decimal_places=2, max_digits=8, validators=[django.core.validators.MinValueValidator(0)], verbose_name='цена продукта на момент заказа'),
        ),
    ]
