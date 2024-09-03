from django.urls import path
from .views import CustomAuthToken, LogoutView, RegisterView, OTPVerifyView

urlpatterns = [
    path('login/', CustomAuthToken.as_view(), name='auth_login'),
    path('logout/', LogoutView.as_view(), name='auth_logout'),
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('verify-otp/', OTPVerifyView.as_view(), name='verify_otp'),
]
