from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .serializers import RegisterSerializer
from .models import Profile, OTP
from .serializers import ProfileSerializer
from .serializers import OTPVerifySerializer
from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import CustomAuthTokenSerializer
from lib.otp import send_otp_sms


class CustomAuthToken(ObtainAuthToken):
    def get_serializer(self):
        return CustomAuthTokenSerializer()

    def post(self, request, *args, **kwargs):
        # Custom authentication using phone number and password
        phone_number = request.data.get('phone_number')
        password = request.data.get('password')

        try:
            profile = Profile.objects.get(phone_number=phone_number)
            user = profile.user
            if not user.check_password(password):
                raise Exception("Invalid password")
        except Profile.DoesNotExist:
            return Response({'error': 'Invalid phone number'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the user is verified
        if not user.profile.is_verified:
            # generate and send OTP
            otp, created = OTP.objects.get_or_create(
                user=user, phone_number=user.profile.phone_number)
            if not created:
                otp.generate_otp()
                otp.save()
            print(f"OTP sent to {user.profile.phone_number}: {otp.otp}")
            send_otp_sms(user.profile.phone_number, otp.otp)
            return Response({
                'error': 'User is not verified. Please complete the verification process.',
                'new otp': otp.otp
            }, status=status.HTTP_403_FORBIDDEN)

        # Delete any existing token for the user
        Token.objects.filter(user=user).delete()

        # Create a new token
        token = Token.objects.create(user=user)

        User.objects.filter(username=user.username).update(
            last_login=timezone.now())
        return Response({
            'role': user.profile.role,
            'token': token.key,
            'user_id': user.pk,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'farmer_id': Profile.objects.filter(user=user).first().id if Profile.objects.filter(user=user).exists() else None
        }, status=status.HTTP_200_OK)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # Get the user's token
            token = Token.objects.get(user=request.user)
            # Delete the token
            token.delete()
            return Response({"message": "Successfully logged out."}, status=status.HTTP_200_OK)
        except Token.DoesNotExist:
            return Response({"error": "Invalid token or already logged out."}, status=status.HTTP_400_BAD_REQUEST)


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if request.data.get('phone_number') and User.objects.filter(profile__phone_number=request.data.get('phone_number')).exists():
            return Response({"error": "Phone number already registered."}, status=status.HTTP_400_BAD_REQUEST)

        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Generate and send OTP
        otp = OTP.objects.create(
            user=user, phone_number=user.profile.phone_number)
        otp.generate_otp()

        # Here you would integrate with an SMS API to send the OTP to the user's phone number
        # Example with Twilio:
        send_otp_sms(user.profile.phone_number, otp.otp)
        print(f"OTP sent to {user.profile.phone_number}: {otp.otp}")

        return Response({
            "user": {
                "username": user.username,
                "phone_number": user.profile.phone_number,
            },
            "otp_message": "OTP has been sent to your phone number. Please verify to complete registration.",
            "otp": otp.otp
        }, status=status.HTTP_201_CREATED)


class OTPVerifyView(generics.GenericAPIView):
    serializer_class = OTPVerifySerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "message": "Phone number verified successfully.",
            "user": {
                "username": user.username,
                "phone_number": user.profile.phone_number,
                "is_verified": user.profile.is_verified,
            }
        }, status=status.HTTP_200_OK)


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filterset_fields = ['user_id']
    search_fields = ['user__username', 'phone_number']
    ordering_fields = ['user__username', 'phone_number']
    ordering = ['user__username']
    lookup_field = 'user_id'
