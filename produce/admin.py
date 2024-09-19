from django.contrib import admin
from .models import Produce, Inventory

@admin.register(Produce)
class ProduceAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'image', 'created_at', 'updated_at')
    search_fields = ('name', 'description')
    list_filter = ('created_at', 'updated_at')
    ordering = ('-created_at',)
    list_per_page = 10
    list_max_show_all = 100
    list_editable = ('description', 'image')
    
    
   
@admin.register(Inventory)   
class InventoryAdmin(admin.ModelAdmin):
    list_display = ('produce', 'quantity', 'created_at', 'updated_at')
    list_filter = ('produce',)
    search_fields = ('produce__name',)
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')

    def save_model(self, request, obj, form, change):
        # Optionally handle custom save logic here
        super().save_model(request, obj, form, change)