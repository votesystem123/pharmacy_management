# Generated by Django 4.2.11 on 2024-03-12 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0013_alter_invoice_invoice_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoiceitem',
            name='batch_id',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
    ]