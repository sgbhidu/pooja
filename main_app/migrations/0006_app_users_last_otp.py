# Generated by Django 4.0.3 on 2022-07-14 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0005_alter_app_users_user_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='app_users',
            name='last_otp',
            field=models.IntegerField(null=True),
        ),
    ]