# Generated by Django 5.1 on 2024-09-10 05:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_remove_order_payment_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='quantity',
            field=models.PositiveIntegerField(blank=True, help_text='Tons', null=True),
        ),
    ]
