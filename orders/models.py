from django.db import models
import uuid
from django.utils import timezone



class Order(models.Model):
    
    ORDER_STATUS = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    )
    
    order_number = models.CharField(max_length=50, unique=True, blank=True, null=True)
    farmer = models.ForeignKey('accounts.Profile', on_delete=models.PROTECT, default=1)
    produce = models.ForeignKey('produce.Produce', on_delete=models.PROTECT, default=1)
    order_description = models.TextField(null=True, blank=True)
    quantity = models.PositiveIntegerField(null=True, blank=True, help_text="Tons")
    order_status = models.CharField(max_length=20, choices=ORDER_STATUS, default='pending')
    order_date = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.order_number:
            date_str = timezone.now().strftime("%Y%m%d")
            unique_id = str(uuid.uuid4().hex[:4]).upper()
            self.order_number = f"ODR-{date_str}-{unique_id}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.farmer} - {self.produce.name} - {self.order_number}"