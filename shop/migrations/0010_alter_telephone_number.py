# Generated by Django 4.0.6 on 2022-11-08 22:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0009_alter_telephone_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='telephone',
            name='number',
            field=models.CharField(max_length=15),
        ),
    ]
