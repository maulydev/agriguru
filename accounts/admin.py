from django.contrib import admin
from .models import Profile, OTP

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'role', 'is_verified', 'phone_number', 'address', 'profile_picture']
    search_fields = ['user__username', 'user__email', 'is_verified', 'phone_number', 'address']
    list_filter = ['role', 'is_verified']
    ordering = ['user__username', 'is_verified',]
    
@admin.register(OTP)
class OTPAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone_number', 'otp', 'created_at']
    search_fields = ['user__username', 'phone_number', 'otp']
    ordering = ['-created_at']