# Generated by Django 4.2.1 on 2023-06-15 06:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bakeryAdmin', '0034_productionorderconsumeproduct'),
    ]

    operations = [
        migrations.AddField(
            model_name='productstock',
            name='measureUnit',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='bakeryAdmin.measureunit'),
        ),
        migrations.AddField(
            model_name='productstock',
            name='unitSellPrice',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5),
        ),
    ]
