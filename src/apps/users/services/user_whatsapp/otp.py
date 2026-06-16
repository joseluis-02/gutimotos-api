# Python
import secrets
# Django
from django.core import signing
from django.utils import timezone
# Models
from apps.core.services.twilio import WhatsAppTwilioService
from ...models.user_whatsapp import UserWhatsApp


def generate_secure_otp() -> str:
    return str(secrets.randbelow(900000) + 100000)  # 100000–999999

def create_signed_otp(contact: UserWhatsApp, ttl_seconds: int = 120) -> str:
    otp = generate_secure_otp()
    contact.otp_signed = signing.dumps(otp)
    contact.otp_expires_at = timezone.now() + timezone.timedelta(seconds=ttl_seconds)
    contact.save(update_fields=["otp_signed", "otp_expires_at"])
    return otp

def send_otp(contact: UserWhatsApp, ttl_seconds: int = 120) -> str:
    otp = create_signed_otp(contact, ttl_seconds)
    WhatsAppTwilioService.send_otp(contact, otp)
    return otp