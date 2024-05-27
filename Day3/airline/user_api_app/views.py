from django.conf import settings
import jwt
from django.contrib.auth import authenticate, login
from rest_framework import generics, status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django_otp.plugins.otp_static.models import StaticDevice, StaticToken
from twilio.rest import Client
import random

from .models import CustomUser, OTPRequest
from .serializers import CustomUserSerializer, OTPRequestSerializer, OTPVerificationSerializer, PasswordResetSerializer, PasswordResetConfirmSerializer

# Utility function to generate OTP
def generate_otp():
    return str(random.randint(100000, 999999))

class CustomUserList(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        # Generate a JWT token for the newly registered user
        user = serializer.instance
        refresh = RefreshToken.for_user(user)

        # Create a response with the token data
        response_data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

        return Response(response_data, status=status.HTTP_201_CREATED)

class CustomUserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_profile(request):
    user = request.user
    data = {
        'email': user.email,
        'country': user.country,
        'age': user.age,
    }
    return Response(data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_user_profile(request):
    user = request.user
    user.country = request.data.get('country', user.country)
    user.age = request.data.get('age', user.age)
    user.save()
    return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(["POST"])
@permission_classes((AllowAny,))
def user_login(request):
    email = request.data.get("email")  # Use 'email' instead of 'username'
    password = request.data.get("password")

    user = authenticate(request, email=email, password=password)  # Use 'email' for authentication
    if user is not None:
        login(request, user)

        # Include user-related data in the JWT payload
        payload = {
            'user_id': user.id,
            'email': user.email,  # Use 'email' field for the JWT payload
            'country': user.country,
            'cnic': user.cnic,
            'phno': user.phno,
            # Include other user-related data here
        }

        # Create and sign the JWT access token
        access_token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

        return Response({"access_token": access_token})
    else:
        return Response(
            {"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
        )

class OTPRequestView(generics.CreateAPIView):
    serializer_class = OTPRequestSerializer

    def post(self, request, *args, **kwargs):
        user = User.objects.get(email=request.data['email'])
        otp_type = request.data['otp_type']
        otp = generate_otp()
        OTPRequest.objects.create(user=user, otp_type=otp_type, otp=otp)

        if otp_type == 'email':
            send_mail(
                'Your OTP Code',
                f'Your OTP code is {otp}',
                'no-reply@yourdomain.com',
                [user.email],
                fail_silently=False,
            )
        elif otp_type == 'sms':
            client = Client(settings.TWILIO_SID, settings.TWILIO_AUTH_TOKEN)
            client.messages.create(
                body=f'Your OTP code is {otp}',
                from_=settings.TWILIO_PHONE_NUMBER,
                to=user.profile.phone_number,  # Assuming you have a phone number field in a Profile model
            )

        return Response({'message': 'OTP sent successfully'}, status=status.HTTP_200_OK)

class OTPVerificationView(generics.GenericAPIView):
    serializer_class = OTPVerificationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            otp = serializer.validated_data['otp']
            otp_request = OTPRequest.objects.filter(user=user, otp=otp, is_verified=False).first()

            if otp_request:
                otp_request.is_verified = True
                otp_request.save()
                payload = {
                    'user_id': user.id,
                    'email': user.email,
                    'country': user.country,
                    'cnic': user.cnic,
                    'phno': user.phno,
                }
                access_token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
                return Response({
                    'access_token': access_token,
                    'user': CustomUserSerializer(user).data
                }, status=status.HTTP_200_OK)
            return Response({'error': 'Invalid OTP or already verified'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PasswordResetView(generics.GenericAPIView):
    serializer_class = PasswordResetSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = User.objects.get(email=email)
            token = default_token_generator.make_token(user)
            reset_link = f'http://localhost:3000/reset-password/{token}'
            send_mail(
                'Password Reset',
                f'Click the link to reset your password: {reset_link}',
                'no-reply@yourdomain.com',
                [user.email],
                fail_silently=False,
            )
            return Response({'message': 'Password reset link sent'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PasswordResetConfirmView(generics.GenericAPIView):
    serializer_class = PasswordResetConfirmSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            token = serializer.validated_data['token']
            new_password = serializer.validated_data['new_password']
            user = User.objects.get(email=serializer.validated_data['email'])
            
            if default_token_generator.check_token(user, token):
                user.set_password(new_password)
                user.save()
                return Response({'message': 'Password reset successful'}, status=status.HTTP_200_OK)
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
