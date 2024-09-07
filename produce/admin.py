from django.contrib import admin
from .models import Produce

@admin.register(Produce)
class ProduceAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'image', 'created_at', 'updated_at')
    search_fields = ('name', 'description')
    list_filter = ('created_at', 'updated_at')
    ordering = ('-created_at',)
    list_per_page = 10
    list_max_show_all = 100
    list_editable = ('description', 'image')