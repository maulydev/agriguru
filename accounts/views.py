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


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        
        # Delete old token if it exists
        Token.objects.filter(user=user).delete()
        
        # Create a new token
        token = Token.objects.create(user=user)
        User.objects.filter(username=user.username).update(last_login=timezone.now())
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'username': user.username
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
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Generate and send OTP
        otp = OTP.objects.create(user=user, phone_number=user.profile.phone_number)
        otp.generate_otp()
        
        # Here you would integrate with an SMS API to send the OTP to the user's phone number
        # Example with Twilio:
        # send_sms(user.profile.phone_number, otp.otp)
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
    filterset_fields = ['user__username']
    search_fields = ['user__username', 'phone_number']
    ordering_fields = ['user__username', 'phone_number']
    ordering = ['user__username']