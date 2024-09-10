from django.contrib import admin
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('payment_reference', 'order', 'amount', 'payment_method', 'payment_status', 'payment_date')
    list_filter = ('payment_method', 'payment_status', 'payment_date')
    search_fields = ('payment_reference', 'order__order_number', 'payment_description')
    readonly_fields = ('payment_reference', 'payment_date')
    fieldsets = (
        (None, {
            'fields': ('order', 'amount', 'payment_method', 'payment_status', 'payment_reference', 'payment_date')
        }),
        ('Additional Information', {
            'fields': ('payment_description',),
        }),
    )
