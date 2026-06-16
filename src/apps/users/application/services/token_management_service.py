# Python
import logging
# Domain
from apps.users.domain.services.token_cleanup_service import TokenCleanupService
logger = logging.getLogger(__name__)

class TokenManagementService:
    """Servicio de aplicación para gestión de tokens"""
    
    @staticmethod
    def cleanup_all_expired_tokens() -> dict:
        """
        Ejecuta limpieza completa de tokens expirados
        
        Returns:
            Diccionario con estadísticas de limpieza
        """
        blacklisted_count = TokenCleanupService.delete_expired_blacklisted_tokens(days=7)
        outstanding_count = TokenCleanupService.delete_expired_outstanding_tokens(days=1)
        
        total = blacklisted_count + outstanding_count
        
        if total > 0:
            logger.info(
                f"Limpieza de tokens completada: "
                f"{blacklisted_count} blacklisted, {outstanding_count} outstanding"
            )
        
        return {
            'blacklisted': blacklisted_count,
            'outstanding': outstanding_count,
            'total': total
        }