from django.contrib import admin
from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'produce', 'expected_quantity', 'location', 'is_sold_out']
    list_filter = ['is_sold_out']
    search_fields = ['title', 'produce__name', 'farmer__user__username']
    list_per_page = 20
    list_max_show_all = 100
    # list_editable = ['is_sold_out']
