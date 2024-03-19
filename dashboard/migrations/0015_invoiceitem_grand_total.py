# Generated by Django 4.2.11 on 2024-03-14 03:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0014_invoiceitem_batch_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoiceitem',
            name='grand_total',
            field=models.DecimalField(decimal_places=2, default=100, max_digits=10),
            preserve_default=False,
        ),
    ]