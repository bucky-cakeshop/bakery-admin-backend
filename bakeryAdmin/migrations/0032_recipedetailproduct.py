# Generated by Django 4.2.1 on 2023-06-12 05:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bakeryAdmin', '0031_product'),
    ]

    operations = [
        migrations.CreateModel(
            name='RecipeDetailProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.DecimalField(decimal_places=2, max_digits=5)),
                ('measureUnit', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='bakeryAdmin.measureunit')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='RecipeDetail_Product', to='bakeryAdmin.product')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='RecipeDetail_Recipe', to='bakeryAdmin.recipe')),
            ],
        ),
    ]