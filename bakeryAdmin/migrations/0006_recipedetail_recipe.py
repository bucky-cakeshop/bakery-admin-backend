# Generated by Django 4.2.1 on 2023-05-19 18:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bakeryAdmin', '0005_recipe_recipedetail'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipedetail',
            name='recipe',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='bakeryAdmin.recipe'),
            preserve_default=False,
        ),
    ]
