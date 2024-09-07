from django.db import models


class Post(models.Model):
    farmer = models.ForeignKey('accounts.Profile', on_delete=models.CASCADE)
    produce = models.ForeignKey('produce.Produce', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(help_text="Tons")
    location = models.CharField(max_length=100)
    description = models.TextField(default='No description')
    is_negotiable = models.BooleanField(default=False)
    expected_quantity = models.PositiveIntegerField(null=True, blank=True, help_text="Tons")
    expected_price_per_unit = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="GHC")
    expected_harvest_date = models.DateTimeField(null=True, blank=True)
    is_sold_out = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.produce.name} - {self.quantity} units"
