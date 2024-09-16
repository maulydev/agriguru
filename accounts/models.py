from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import random
import string


class Profile(models.Model):
    ROLE_CHOICES = [
        ('farmer', 'Farmer'),
        ('expert', 'Expert'),
        ('admin', 'Admin'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=ROLE_CHOICES[0][0])
    phone_number = models.CharField(max_length=15, blank=True, null=True, unique=True)
    address = models.TextField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

class OTP(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(default=timezone.now)

    def is_expired(self):
        return timezone.now() > self.created_at + timezone.timedelta(minutes=10)

    def generate_otp(self):
        self.otp = ''.join(random.choices(string.digits, k=6))
        self.created_at = timezone.now()
        self.save()

    def __str__(self):
        return f"{self.user.profile.phone_number} - {self.otp}"
