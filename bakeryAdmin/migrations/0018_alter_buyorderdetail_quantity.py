# Generated by Django 4.2.1 on 2023-05-24 06:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bakeryAdmin', '0017_buyorder_buyorderdetail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buyorderdetail',
            name='quantity',
            field=models.DecimalField(decimal_places=2, max_digits=5),
        ),
    ]
