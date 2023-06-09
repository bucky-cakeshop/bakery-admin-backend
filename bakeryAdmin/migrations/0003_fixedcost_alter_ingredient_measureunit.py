# Generated by Django 4.2.1 on 2023-05-18 19:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bakeryAdmin', '0002_ingredient'),
    ]

    operations = [
        migrations.CreateModel(
            name='FixedCost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=5)),
            ],
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='measureUnit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='bakeryAdmin.measureunit'),
        ),
    ]
