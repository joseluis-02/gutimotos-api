# Python
import logging
# Domain
from apps.core.domain.services.session_cleanup_service import SessionCleanupService

logger = logging.getLogger(__name__)

class InfrastructureCleanupService:
    """Servicio de aplicación para limpieza de infraestructura Django"""
    
    @staticmethod
    def cleanup_expired_sessions() -> dict:
        """
        Limpia sesiones expiradas
        
        Returns:
            Diccionario con estadísticas
        """
        sessions = SessionCleanupService.delete_expired_sessions()
        
        if sessions > 0:
            logger.info(f"Limpieza de sesiones completada: {sessions} eliminadas")
        
        return {
            'sessions': sessions,
            'total': sessions
        }