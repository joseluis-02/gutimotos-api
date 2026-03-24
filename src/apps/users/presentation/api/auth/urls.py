
from django.urls import path
from apps.users.presentation.api.auth.views.otp_views import (
    RequestOTPView,
    VerifyOTPView
)
app_name = 'auth'
urlpatterns = [
    # OTP Authentication
    path('api/auth/otp/request/', RequestOTPView.as_view(), name='otp_request'),
    path('api/auth/otp/verify/', VerifyOTPView.as_view(), name='otp_verify'),
]