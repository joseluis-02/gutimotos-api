# Python
import logging
# Django
from django.core.mail import EmailMessage
from django.conf import settings

logger = logging.getLogger(__name__)

class EmailService:
    """Servicio reutilizable para envío de emails con Anymail/SES"""
    
    @staticmethod
    def send_email_with_attachment(
        to_email: str,
        subject: str,
        html_content: str,
        attachment_data: bytes = None,
        attachment_name: str = None,
        attachment_type: str = 'application/pdf'
    ) -> bool:
        """
        Envía email con archivo adjunto opcional
        
        Args:
            to_email: Email destino
            subject: Asunto
            html_content: Contenido HTML
            attachment_data: Bytes del archivo (opcional)
            attachment_name: Nombre del archivo (opcional)
            attachment_type: Tipo MIME
            
        Returns:
            True si se envió correctamente
        """
        try:
            email = EmailMessage(
                subject=subject,
                body=html_content,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[to_email]
            )
            email.content_subtype = 'html'
            
            # Agregar adjunto solo si se proporciona
            if attachment_data and attachment_name:
                email.attach(attachment_name, attachment_data, attachment_type)
            
            email.send()
            
            logger.info(f"Email enviado exitosamente a {to_email}")
            return True
            
        except Exception as e:
            logger.error(f"Error enviando email a {to_email}: {str(e)}")
            return False