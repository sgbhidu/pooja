# Generated by Django 4.2 on 2023-07-28 18:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0022_saved_address_name_saved_address_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='color_quantity',
            name='slug',
            field=models.SlugField(null=True, unique=True),
        ),
    ]
