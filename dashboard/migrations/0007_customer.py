# Generated by Django 4.2.11 on 2024-03-08 12:02

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0006_medicine'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128, null=True, region=None, unique=True)),
                ('dr_name', models.CharField(max_length=100)),
                ('dr_dept', models.CharField(max_length=100)),
                ('dr_address', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'customer',
                'verbose_name_plural': 'customer',
            },
        ),
    ]
