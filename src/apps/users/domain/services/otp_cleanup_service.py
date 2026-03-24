# Python
import logging
# Users - Infrastructure
from apps.users.infrastructure.persistence.repositories.otp_repository_impl import OTPRepositoryImpl

logger = logging.getLogger(__name__)


class OTPCleanupService:
    """Servicio para limpieza de OTPs expirados"""
    
    @staticmethod
    def delete_expired_otps(days: int = 1) -> int:
        """
        Elimina OTPs expirados antiguos
        
        Args:
            days: Eliminar OTPs expirados hace más de X días
            
        Returns:
            Cantidad eliminada
        """
        repository = OTPRepositoryImpl()
        count = repository.delete_expired(days)
        
        if count > 0:
            logger.info(f"Limpieza de OTPs: {count} eliminados")
        
        return count