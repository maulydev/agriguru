# Generated by Django 5.1 on 2024-09-10 04:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_remove_order_payment_method_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='payment_date',
        ),
    ]
