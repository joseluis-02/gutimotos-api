# Python
import logging
import uuid
# Django
from django.template.loader import render_to_string
from django.conf import settings
from django.utils import timezone
from django.core.mail import EmailMultiAlternatives

logger = logging.getLogger(__name__)


class OTPEmailService:
    """Servicio minimalista para envío de OTP"""
    
    @staticmethod
    def send_otp_email(
        email: str,
        otp_code: str,
        action: str = 'login',
        validity_minutes: int = 10
    ) -> bool:
        """Envía email OTP estilo minimalista"""
        try:
            context = {
                'otp_code': otp_code,
                'company_name': 'Gutimotos',
                'current_year': timezone.now().year,
                'validity_minutes': validity_minutes,
            }
            
            html_content = render_to_string('users/email/otp_code.html', context)
            
            text_content = f"""Gutimotos

Usa este código para verificar tu identidad:

{otp_code}

Este código expira en {validity_minutes} minutos.

Si no solicitaste este código, ignora este correo.

Gutimotos • {context['current_year']}"""
            
            # Subject SIN código (cambio clave anti-spam)
            subject = "Gutimotos - Código de verificación"
            
            email_message = EmailMultiAlternatives(
                subject=subject,
                body=text_content,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[email],
                headers={
                    "X-Mailer": "Amazon SES",
                    "X-Entity-Ref-ID": str(uuid.uuid4()),
                }
            )
            
            email_message.attach_alternative(html_content, "text/html")
            email_message.send(fail_silently=False)
            
            logger.info(f"OTP enviado a {email} (action: {action})")
            return True
            
        except Exception as e:
            logger.exception(f"Error enviando OTP: {e}")
            return False