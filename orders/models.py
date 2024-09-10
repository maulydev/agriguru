from django.db import models


class Order(models.Model):
    
    ORDER_STATUS = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    )
    
    farmer = models.CharField(max_length=50, default='')
    produce = models.ForeignKey('produce.Produce', on_delete=models.PROTECT, default=1)
    order_description = models.TextField(null=True, blank=True)
    quantity = models.PositiveIntegerField(null=True, blank=True, help_text="Tons")
    order_status = models.CharField(max_length=20, choices=ORDER_STATUS, default='pending')
    order_date = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.farmer} - {self.produce.name}"