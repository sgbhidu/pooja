# Generated by Django 4.0.3 on 2022-08-22 08:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0007_app_users_user_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='pooja_products',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('size', models.CharField(max_length=50)),
                ('description', models.TextField()),
            ],
        ),
    ]
