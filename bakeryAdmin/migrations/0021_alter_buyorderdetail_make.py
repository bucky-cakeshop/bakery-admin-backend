# Generated by Django 4.2.1 on 2023-05-24 19:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bakeryAdmin', '0020_buyorderdetail_make'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buyorderdetail',
            name='make',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.DO_NOTHING, to='bakeryAdmin.make'),
        ),
    ]
