from django.contrib import admin
from .models import PurchaseRequest, PurchaseResponse


@admin.register(PurchaseRequest)
class PurchaseRequestAdmin(admin.ModelAdmin):
    list_display = ('factory', 'produce', 'quantity_requested', 'pickup_date', 'status')
    list_filter = ('status',)
    search_fields = ('factory__phone_number', 'produce__name')


@admin.register(PurchaseResponse)
class PurchaseResponseAdmin(admin.ModelAdmin):
    list_display = ('purchase_request', 'farmer', 'accepted')
    search_fields = ('farmer__phone_number', 'purchase_request__id')