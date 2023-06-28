# Generated by Django 4.2.1 on 2023-06-19 08:39

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('bakeryAdmin', '0036_rename_productionstock_productionorderconsumeproduct_productstock'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='measureUnit',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='bakeryAdmin.measureunit'),
        ),
        migrations.AddField(
            model_name='productstock',
            name='creationAt',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='productstock',
            name='updatedAt',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]