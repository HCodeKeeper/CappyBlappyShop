# Generated by Django 4.0.1 on 2022-08-24 13:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deal',
            name='product',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='shop.product'),
        ),
    ]
