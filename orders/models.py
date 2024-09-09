from django.db import models


class Order(models.Model):
    
    ORDER_STATUS = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    )
    
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
    
    post = models.ForeignKey('posts.Post', on_delete=models.CASCADE)
    order_status = models.CharField(max_length=20, choices=ORDER_STATUS, default='pending')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD, default='cash')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='pending')
    payment_date = models.DateTimeField(null=True, blank=True)
    order_date = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.farmer.user.username} - {self.post.title}"