from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=100, null=True, blank=True)
    farmer = models.ForeignKey('accounts.Profile', on_delete=models.CASCADE)
    produce = models.ForeignKey('produce.Produce', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='posts/images/', null=True, blank=True)
    location = models.CharField(max_length=100)
    description = models.TextField(default='No description')
    is_negotiable = models.BooleanField(default=False)
    expected_quantity = models.PositiveIntegerField(null=True, blank=True, help_text="Tons")
    price_per_ton = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="GHC")
    expected_harvest_date = models.DateTimeField(null=True, blank=True)
    is_sold_out = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.produce.name} - {self.expected_quantity} tons"
