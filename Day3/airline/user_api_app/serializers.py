from django.contrib.auth import get_user_model  # Import the User model
from rest_framework import serializers
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.conf import settings
from .models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()  # Use get_user_model to access the user model
        fields = ("id", "email", "password", "age", "country")
        extra_kwargs = {
            "password": {"write_only": True, "style": {"input_type": "password"}}
        }

    def validate_email(self, value):
        User = get_user_model()
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email address is already in use.")
        return value

    def create(self, validated_data):
        user = get_user_model().objects.create_user(
            email=validated_data["email"],
            country=validated_data["country"],
            age=validated_data["age"],
            password=validated_data["password"],
        )

        return user

    def update(self, instance, validated_data):
        """Handle updating user account"""
        if "password" in validated_data:
            password = validated_data.pop("password")
            instance.set_password(password)

        return super().update(instance, validated_data)
    
class OTPRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

class OTPVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)

class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("User with this email does not exist.")
        return value

    def save(self):
        user = CustomUser.objects.get(email=self.validated_data['email'])
        token = default_token_generator.make_token(user)
        reset_url = f"{settings.FRONTEND_URL}/password-reset-confirm/{token}/"
        send_mail(
            "Password Reset Request",
            f"Use the following link to reset your password: {reset_url}",
            settings.DEFAULT_FROM_EMAIL,
            [user.email]
        )

class PasswordResetConfirmSerializer(serializers.Serializer):
    token = serializers.CharField()
    new_password = serializers.CharField(write_only=True)

    def validate(self, data):
        try:
            user = CustomUser.objects.get(email=self.context['email'])
            if not default_token_generator.check_token(user, data['token']):
                raise serializers.ValidationError("Invalid or expired token.")
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("Invalid token.")
        return data

    def save(self):
        user = CustomUser.objects.get(email=self.context['email'])
        user.set_password(self.validated_data['new_password'])
        user.save()