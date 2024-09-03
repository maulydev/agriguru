from django.contrib import admin
from .models import Profile, OTP

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'role', 'phone_number', 'address', 'profile_picture']
    search_fields = ['user__username', 'user__email', 'phone_number', 'address']
    list_filter = ['role']
    ordering = ['user__username']
    
@admin.register(OTP)
class OTPAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone_number', 'otp', 'created_at']
    search_fields = ['user__username', 'phone_number', 'otp']
    ordering = ['-created_at']