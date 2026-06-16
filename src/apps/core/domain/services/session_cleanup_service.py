# Python
import logging
# Django
from django.utils import timezone

logger = logging.getLogger(__name__)


class SessionCleanupService:
    """Servicio de dominio para limpieza de sesiones de Django"""
    
    @staticmethod
    def delete_expired_sessions() -> int:
        """
        Elimina sesiones expiradas de Django
        
        Django guarda sesiones en BD que se acumulan con el tiempo.
        Este método elimina las que ya expiraron.
        
        Returns:
            Cantidad de sesiones eliminadas
        """
        try:
            from django.contrib.sessions.models import Session
            
            # Eliminar sesiones cuya fecha de expiración ya pasó
            now = timezone.now()
            expired_sessions = Session.objects.filter(expire_date__lt=now)
            count = expired_sessions.count()
            
            if count > 0:
                expired_sessions.delete()
                logger.info(f"{count} sesiones expiradas eliminadas")
            
            return count
            
        except Exception as e:
            logger.exception(f"Error eliminando sesiones: {str(e)}")
            return 0