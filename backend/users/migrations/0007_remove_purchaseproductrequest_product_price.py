# Generated by Django 3.1.13 on 2021-08-31 17:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_auto_20210831_1714'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='purchaseproductrequest',
            name='product_price',
        ),
    ]
