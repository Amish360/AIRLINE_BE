from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
import phonenumbers
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("email address"), unique=True)
    cnic = models.BigIntegerField(default=False)  # Assuming CNIC is a large number
    phno = models.BigIntegerField(default=False)  # Assuming phone number can be large, removing max_length
    age = models.PositiveIntegerField(default=False)  # Age should be positive
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        if self.phno:
            try:
                parsed_number = phonenumbers.parse(self.phno, None)
                if not phonenumbers.is_valid_number(parsed_number):
                    raise ValidationError("Invalid phone number")
                self.phno = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164)
            except phonenumbers.phonenumberutil.NumberParseException as e:
                raise ValidationError(f"Error parsing phone number: {e}")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email
    

class OTPRequest(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    otp_type = models.CharField(max_length=10)  # 'email' or 'sms'
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)