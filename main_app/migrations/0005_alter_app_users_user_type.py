# Generated by Django 4.0.3 on 2022-07-14 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0004_alter_app_users_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='app_users',
            name='user_type',
            field=models.CharField(choices=[('Admin', 'Admin'), ('Customer', 'Customer')], default='Customer', max_length=10),
        ),
    ]
