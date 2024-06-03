import random
import string
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone

def generate_otp():
    return ''.join(random.choices(string.digits, k=6))

def send_otp_email(user):
    otp = generate_otp()
    user.otp = otp
    user.otp_expiration = timezone.now() + timezone.timedelta(minutes=10)
    user.save()
    subject = 'Your OTP Code'
    message = f'Your OTP code is {otp}. It will expire in 10 minutes.'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [user.email]
    send_mail(subject, message, email_from, recipient_list)
