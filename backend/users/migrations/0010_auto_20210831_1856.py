# Generated by Django 3.1.13 on 2021-08-31 18:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_product_first_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='first_quantity',
            field=models.IntegerField(verbose_name='First Quantity'),
        ),
    ]
