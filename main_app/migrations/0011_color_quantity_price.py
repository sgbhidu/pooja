# Generated by Django 4.0.3 on 2022-08-25 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0010_color_quantity_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='color_quantity',
            name='price',
            field=models.IntegerField(default=0),
        ),
    ]
