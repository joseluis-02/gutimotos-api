# Django
from django.db import models

class MethodTypeOtp(models.TextChoices):
    EMAIL_OTP = "email_otp", "Email OTP"
    WHATSAPP_OTP = "whatsapp_otp", "WhatsApp OTP"
    SMS_OTP = "sms_otp", "SMS OTP"