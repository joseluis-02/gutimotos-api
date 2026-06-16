# Django
from django.utils import timezone
from datetime import timedelta
import logging

logger = logging.getLogger(__name__)


class TokenCleanupService:
    """Servicio de dominio para limpieza de tokens JWT"""
    
    @staticmethod
    def delete_expired_blacklisted_tokens(days: int = 7) -> int:
        """
        Elimina tokens en blacklist que expiraron hace X días
        
        Args:
            days: Días después de expiración para eliminar
            
        Returns:
            Cantidad de tokens eliminados
        """
        try:
            from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken
            
            cutoff_date = timezone.now() - timedelta(days=days)
            #cutoff_date = timezone.now() - timedelta(minutes=1)
            
            old_blacklisted = BlacklistedToken.objects.filter(
                token__expires_at__lt=cutoff_date
            )
            
            count = old_blacklisted.count()
            
            if count > 0:
                old_blacklisted.delete()
                logger.info(f"{count} tokens blacklisteados eliminados")
            
            return count
            
        except Exception as e:
            logger.exception(f"Error eliminando tokens blacklisteados: {str(e)}")
            return 0
    
    @staticmethod
    def delete_expired_outstanding_tokens(days: int = 1) -> int:
        """
        Elimina outstanding tokens que expiraron hace X días
        
        Args:
            days: Días después de expiración para eliminar
            
        Returns:
            Cantidad de tokens eliminados
        """
        try:
            from rest_framework_simplejwt.token_blacklist.models import OutstandingToken
            
            cutoff_date = timezone.now() - timedelta(days=days)
            #cutoff_date = timezone.now() - timedelta(minutes=1)
            
            expired_tokens = OutstandingToken.objects.filter(
                expires_at__lt=cutoff_date
            )
            
            count = expired_tokens.count()
            
            if count > 0:
                expired_tokens.delete()
                logger.info(f"{count} outstanding tokens eliminados")
            
            return count
            
        except Exception as e:
            logger.exception(f"Error eliminando outstanding tokens: {str(e)}")
            return 0