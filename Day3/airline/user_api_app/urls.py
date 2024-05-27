from django.urls import path

from .views import (
    CustomUserDetail, 
    CustomUserList, 
    user_login, 
    get_user_profile, 
    update_user_profile,
    OTPRequestView,
    OTPVerificationView,
    PasswordResetView,
    PasswordResetConfirmView,
)

urlpatterns = [
    path("register/", CustomUserList.as_view(), name="user-list"),
    path("register/<int:pk>/", CustomUserDetail.as_view(), name="user-detail"),
    path('get_user_profile/', get_user_profile, name='get_user_profile'),
    path('update_user_profile/', update_user_profile, name='update_user_profile'),
    path("login/", user_login, name="user_login"),
    path("otp-request/", OTPRequestView.as_view(), name="otp_request"),
    path("otp-verify/", OTPVerificationView.as_view(), name="otp_verify"),
    path("password-reset/", PasswordResetView.as_view(), name="password_reset"),
    path("password-reset-confirm/", PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
]
