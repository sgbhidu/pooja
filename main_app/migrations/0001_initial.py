# Generated by Django 4.0.3 on 2022-07-10 14:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='app_users',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('phone', models.IntegerField()),
                ('alternate_phone', models.IntegerField()),
                ('email', models.EmailField(max_length=254)),
                ('password', models.CharField(max_length=100)),
                ('anniversary', models.DateField()),
                ('date_of_birth', models.DateField()),
                ('user_type', models.CharField(choices=[('Admin', 'Admin'), ('Customer', 'Customer')], default='Admin', max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='permanent_Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=200)),
                ('landmark', models.CharField(max_length=200)),
                ('pincode', models.IntegerField()),
                ('city', models.CharField(max_length=200)),
                ('state', models.CharField(max_length=200)),
                ('country', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='saved_Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=200)),
                ('landmark', models.CharField(max_length=200)),
                ('pincode', models.IntegerField()),
                ('city', models.CharField(max_length=200)),
                ('state', models.CharField(max_length=200)),
                ('country', models.CharField(max_length=200)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.app_users')),
            ],
        ),
        migrations.AddField(
            model_name='app_users',
            name='permanent_Address',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='main_app.permanent_address'),
        ),
    ]
