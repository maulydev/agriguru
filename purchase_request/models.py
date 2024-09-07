from django.db import models
from django.contrib.auth.models import User
from produce.models import Produce

STATUS_CHOICES = [('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')]

class PurchaseRequest(models.Model):
    factory = models.ForeignKey(User, on_delete=models.CASCADE)  # Only factory
    produce = models.ForeignKey(Produce, on_delete=models.CASCADE)
    quantity_requested = models.PositiveIntegerField()
    proposed_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    pickup_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    farmers_responded = models.ManyToManyField(User, through='PurchaseResponse', related_name='responses')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Request for {self.produce} by {self.factory.username}"



class PurchaseResponse(models.Model):
    purchase_request = models.ForeignKey(PurchaseRequest, on_delete=models.CASCADE)
    farmer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='purchase_responses')
    accepted = models.BooleanField(default=False)
    response_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Response by {self.farmer.username} for request {self.purchase_request.id}"

