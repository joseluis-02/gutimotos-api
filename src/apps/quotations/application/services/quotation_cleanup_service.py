# Python
from datetime import timedelta
# Django
from django.utils import timezone
from apps.quotations.infrastructure.persistence.models.quotation import Quotation
from apps.quotations.domain.choices.quotation_status import QuotationStatus
import logging

logger = logging.getLogger(__name__)


class QuotationCleanupService:
    """Servicio para limpieza de cotizaciones"""
    
    @staticmethod
    def delete_cancelled_quotations() -> int:
        """
        Elimina TODAS las cotizaciones canceladas
        
        Returns:
            Cantidad de cotizaciones eliminadas
        """
        cancelled = Quotation.objects.filter(status=QuotationStatus.CANCELLED)
        count = cancelled.count()
        
        if count > 0:
            cancelled.delete()
            logger.info(f"{count} cotizaciones canceladas eliminadas")
        
        return count
    
    @staticmethod
    def delete_old_expired_quotations(days: int = 7) -> int:
        """
        Elimina cotizaciones expiradas con más de X días de antigüedad
        
        Args:
            days: Días desde que expiró (default: 7)
            
        Returns:
            Cantidad de cotizaciones eliminadas
        """
        #cutoff_date = timezone.now() - timedelta(days=days)
        cutoff_date = timezone.now() - timedelta(minutes=20)
        
        old_expired = Quotation.objects.filter(
            status=QuotationStatus.EXPIRED,
            expired__lt=cutoff_date  # Expiró hace más de 7 días
        )
        
        count = old_expired.count()
        
        if count > 0:
            old_expired.delete()
            logger.info(f"{count} cotizaciones expiradas eliminadas")
        
        return count