# Generated by Django 4.2.11 on 2024-05-05 20:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_alter_products_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='Price',
            field=models.FloatField(default=0),
        ),
    ]