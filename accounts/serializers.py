from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile, OTP


class CustomAuthTokenSerializer(serializers.Serializer):
    phone_number = serializers.CharField(label="Phone Number")
    password = serializers.CharField(label="Password", style={
                                     'input_type': 'password'}, trim_whitespace=False)


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={
                                     'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, required=True, style={
                                      'input_type': 'password'}, label="Confirm password")
    phone_number = serializers.CharField(
        write_only=True, required=True, label="Phone Number")

    class Meta:
        model = User
        fields = ('username', 'phone_number', 'password', 'password2')

    def validate(self, data):
        # if data["phone_number"] and User.objects.filter(profile__phone_number=data["phone_number"]).exists():
        #     raise serializers.ValidationError("Phone number already registered.")

        if data['password'] != data['password2']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        Profile.objects.create(
            user=user, phone_number=validated_data['phone_number'])
        return user


class OTPVerifySerializer(serializers.Serializer):
    otp = serializers.CharField(max_length=6)
    phone_number = serializers.CharField(max_length=15)

    def validate(self, data):
        try:
            user = User.objects.get(profile__phone_number=data['phone_number'])
            otp_record = OTP.objects.get(
                user=user, phone_number=data['phone_number'], otp=data['otp'])
            if otp_record.is_expired():
                raise serializers.ValidationError("OTP has expired.")
        except (User.DoesNotExist, OTP.DoesNotExist):
            raise serializers.ValidationError("Invalid OTP or phone number.")
        return data

    def save(self):
        user = User.objects.get(
            profile__phone_number=self.validated_data['phone_number'])
        user.profile.is_verified = True
        user.profile.save()
        # Clean up OTP record after verification
        OTP.objects.filter(user=user).delete()
        return user


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'