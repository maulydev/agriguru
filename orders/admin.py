from django.contrib import admin
from .models import Order

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('farmer', 'produce', 'quantity', 'order_status', 'order_date', 'last_updated')
    list_filter = ('order_status', 'order_date')
    search_fields = ('farmer', 'produce', 'quantity', 'order_status')
    readonly_fields = ('order_date', 'last_updated')
    date_hierarchy = 'order_date'

