# models.py

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager
import random
import string
import datetime


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("email address"), unique=True)
    cnic = models.BigIntegerField(default=False)  # Assuming CNIC is a large number
    age = models.PositiveIntegerField(default=False)  # Age should be positive
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    otp = models.CharField(max_length=6, blank=True, null=True)
    otp_expiration = models.DateTimeField(blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def generate_otp(self):
        self.otp = ''.join(random.choices(string.digits, k=6))
        self.otp_expiration = timezone.now() + datetime.timedelta(minutes=10)
        self.save()
