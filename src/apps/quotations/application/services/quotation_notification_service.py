# Python
import logging
from datetime import timedelta
from collections import defaultdict
# Django
from django.utils import timezone
from django.template.loader import render_to_string
from django.conf import settings
# Models
from apps.quotations.infrastructure.persistence.models.quotation import Quotation
from apps.quotations.domain.choices.quotation_status import QuotationStatus
# Core
from apps.core.services.email_service import EmailService


logger = logging.getLogger(__name__)


class QuotationNotificationService:
    """Servicio para notificaciones de cotizaciones"""
    
    @staticmethod
    def notify_expiring_quotations(hours_before: int = 24) -> int:
        """
        Notifica a clientes sobre cotizaciones próximas a expirar
        
        Args:
            hours_before: Horas antes de expirar para notificar (default: 24)
            
        Returns:
            Cantidad de usuarios notificados
        """
        now = timezone.now()
        #expiration_threshold = now + timedelta(hours=hours_before)
        expiration_threshold = now + timedelta(minutes=5)
        
        # Obtener cotizaciones próximas a expirar sin notificación previa
        expiring_quotations = Quotation.objects.filter(
            status=QuotationStatus.REVIEWED,
            expired__gte=now,
            expired__lte=expiration_threshold,
            notification_sent=False
        ).select_related('user').only(
            'id', 'user', 'expired', 'currency_code', 'total', 'notification_sent'
        )
        
        if not expiring_quotations.exists():
            logger.info("No hay cotizaciones próximas a expirar")
            return 0
        
        # Agrupar por usuario para enviar un solo email por usuario
        quotations_by_user = defaultdict(list)
        for quotation in expiring_quotations:
            quotations_by_user[quotation.user].append(quotation)
        
        # Procesar envíos
        return QuotationNotificationService._process_notifications(
            quotations_by_user, 
            hours_before
        )
    
    @staticmethod
    def _process_notifications(quotations_by_user: dict, hours_before: int) -> int:
        """
        Procesa y envía notificaciones a cada usuario
        
        Args:
            quotations_by_user: Diccionario de usuario -> lista de cotizaciones
            hours_before: Horas antes de expirar
            
        Returns:
            Cantidad de usuarios notificados
        """
        notified_count = 0
        
        for user, quotations in quotations_by_user.items():
            try:
                # Enviar notificación
                success = QuotationNotificationService._send_expiration_warning_email(
                    user=user,
                    quotations=quotations,
                    hours_remaining=hours_before
                )
                
                if success:
                    # Marcar como notificadas en una sola query
                    quotation_ids = [q.id for q in quotations]
                    Quotation.objects.filter(id__in=quotation_ids).update(
                        notification_sent=True
                    )
                    
                    notified_count += 1
                    logger.info(
                        f"Notificación enviada a {user.email} - "
                        f"{len(quotations)} cotización(es)"
                    )
                else:
                    logger.warning(f"Falló envío a {user.email}")
                    
            except Exception as e:
                logger.exception(f"Error notificando a {user.email}: {str(e)}")
        
        return notified_count
    
    @staticmethod
    def _send_expiration_warning_email(user, quotations: list, hours_remaining: int) -> bool:
        """
        Envía email de advertencia de expiración
        
        Args:
            user: Usuario destinatario
            quotations: Lista de cotizaciones del usuario
            hours_remaining: Horas restantes antes de expirar
            
        Returns:
            True si el envío fue exitoso
        """
        try:
            quotations_count = len(quotations)
            # Preparar mensaje de WhatsApp
            if quotations_count == 1:
                whatsapp_message = f"Necesito ayuda con mi cotización que está por expirar."
            else:
                whatsapp_message = f"Necesito ayuda con mis {quotations_count} cotizaciones que están por expirar."
            
            # Link de WhatsApp
            support_phone_number = '59167398260'
            whatsapp_link = f"https://wa.me/{support_phone_number}?text={whatsapp_message}"
            
            
            # Contexto del template
            context = {
                'quotations': quotations,
                'quotations_count': quotations_count,
                'is_single': quotations_count == 1,
                'hours_remaining': hours_remaining,
                'web_url': 'https://gutimotos.com',
                'company_name': 'Gutimotos',
                'support_phone': '67398260',
                'whatsapp_link': whatsapp_link,
                'current_year': timezone.now().year,
            }
            
            # Renderizar HTML
            html_content = render_to_string(
                'quotations/email/quotation_expiration_warning.html',
                context
            )
            
            # Subject dinámico
            if quotations_count == 1:
                subject = "Tu cotización está por expirar"
            else:
                subject = f"Tienes {quotations_count} cotizaciones por expirar"
            
            # Enviar email
            return EmailService.send_email_with_attachment(
                to_email=user.email,
                subject=subject,
                html_content=html_content,
                attachment_data=None,
                attachment_name=None
            )
            
        except Exception as e:
            logger.exception(f"Error generando email para {user.email}: {str(e)}")
            return False