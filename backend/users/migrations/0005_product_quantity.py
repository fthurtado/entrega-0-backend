# Generated by Django 3.1.13 on 2021-08-31 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20210831_1646'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='quantity',
            field=models.IntegerField(default=5, verbose_name='Quantity'),
        ),
    ]
