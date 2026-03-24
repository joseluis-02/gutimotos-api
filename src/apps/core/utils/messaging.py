from django.core.mail import send_mail
from django.conf import settings
from typing import Optional
import logging

logger = logging.getLogger(__name__)

# ----------------------
# Envío de Email OTP
# ----------------------
def send_email_otp(
    to_email: str, 
    otp_code: str, 
    subject: Optional[str] = None, 
    body: Optional[str] = None
):
    """
    Envía un código OTP por correo electrónico.
    """
    subject = subject or "Código OTP de verificación"
    body = body or f"Tu código OTP es {otp_code}. Expira en 2 minutos."

    try:
        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [to_email],
            fail_silently=False
        )
        logger.info(f"OTP enviado a {to_email}")
    except Exception as e:
        logger.error(f"No se pudo enviar OTP a {to_email}: {e}")
        raise
