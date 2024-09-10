from django.db import models
from django.contrib.auth.models import User
from produce.models import Produce
from accounts.models import Profile
from django.db.models.signals import post_save
from django.dispatch import receiver


STATUS_CHOICES = [('pending', 'Pending'), ('cancelled', 'Cancelled'), ('completed', 'Completed')]

class PurchaseRequest(models.Model):
    produce = models.ForeignKey(Produce, on_delete=models.CASCADE)
    quantity_requested = models.PositiveIntegerField(help_text='Quantity in tons')
    proposed_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text='Price per ton')
    pickup_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    farmers_responded = models.ManyToManyField('accounts.Profile', through='PurchaseResponse', related_name='responses')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Request for {self.produce}"


class PurchaseResponse(models.Model):
    purchase_request = models.ForeignKey(PurchaseRequest, on_delete=models.CASCADE)
    farmer = models.ForeignKey('accounts.Profile', on_delete=models.CASCADE, related_name='purchase_responses')
    accepted = models.BooleanField(default=False)
    rejected = models.BooleanField(default=False)
    response_date = models.DateTimeField(auto_now_add=True)
    price_per_ton = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text='Price per ton')

    def __str__(self):
        return f"Response by {self.farmer.user.username} for request {self.purchase_request.id}"


@receiver(post_save, sender=PurchaseRequest)
def create_purchase_responses(sender, instance, created, **kwargs):
    if created:
        farmers = Profile.objects.filter(role='farmer')
        for farmer in farmers:
            PurchaseResponse.objects.create(
                purchase_request=instance,
                farmer=farmer
            )