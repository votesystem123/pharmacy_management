# Generated by Django 4.2.11 on 2024-03-12 06:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0010_customer_date_created'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invoice',
            name='amount',
        ),
        migrations.RemoveField(
            model_name='invoice',
            name='medicine',
        ),
        migrations.RemoveField(
            model_name='invoice',
            name='quantity',
        ),
    ]
