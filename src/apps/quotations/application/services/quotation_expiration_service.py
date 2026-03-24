# Django
from django.utils import timezone
from apps.quotations.infrastructure.persistence.models.quotation import Quotation
from apps.quotations.domain.choices.quotation_status import QuotationStatus
import logging

logger = logging.getLogger(__name__)


class QuotationExpirationService:
    """Servicio para expirar cotizaciones vencidas"""
    
    @staticmethod
    def expire_quotations() -> int:
        """
        Marca como EXPIRED las cotizaciones vencidas
        
        Returns:
            Cantidad de cotizaciones expiradas
        """
        now = timezone.now()
        
        expired_quotations = Quotation.objects.filter(
            expired__lt=now,
            status__in=[QuotationStatus.CREATED, QuotationStatus.REVIEWED]
        )
        
        count = expired_quotations.count()
        
        if count > 0:
            expired_quotations.update(status=QuotationStatus.EXPIRED)
            logger.info(f"{count} cotizaciones marcadas como EXPIRED")
        
        return count