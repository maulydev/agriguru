from django.db import models
import uuid
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver


class Payment(models.Model):
    
    PAYMENT_METHOD = (
        ('cash', 'Cash'),
        ('momo', 'Momo'),
        ('bank', 'Bank')
    )
    
    PAYMENT_STATUS = (
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
    )
    
    order = models.OneToOneField('orders.Order', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD, default='cash')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='pending')
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_reference = models.CharField(max_length=100, unique=True, blank=True)
    payment_description = models.TextField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.payment_reference:
            date_str = timezone.now().strftime("%Y%m%d")
            unique_id = uuid.uuid4().hex[:8].upper()
            self.payment_reference = f"PAY-{date_str}-{unique_id}"

        super().save(*args, **kwargs)

    def __str__(self):
        return self.payment_reference


@receiver(post_save, sender=Payment)
def update_order_status(sender, instance, created, **kwargs):
    if not created:
        order = instance.order
        if instance.payment_status == 'paid':
            order.order_status = 'completed'
        else:
            order.order_status = 'pending'
        order.save()