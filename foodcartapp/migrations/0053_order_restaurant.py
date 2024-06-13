# Generated by Django 3.2.15 on 2024-05-18 16:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0052_alter_order_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='restaurant',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='foodcartapp.restaurant', verbose_name='ресторан'),
        ),
    ]