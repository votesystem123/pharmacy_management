# Generated by Django 4.2.11 on 2024-03-14 10:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0017_alter_invoice_grand_total'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customer',
            old_name='dr_address',
            new_name='dr_hospital',
        ),
    ]