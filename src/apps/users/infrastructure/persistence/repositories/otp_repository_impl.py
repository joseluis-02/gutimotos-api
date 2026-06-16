# Python
import logging
from typing import Optional
from datetime import timedelta
# Django
from django.utils import timezone
# Domain
from apps.users.domain.repositories.otp_repository import IOTPRepository
# Infrastructure
from apps.users.infrastructure.persistence.models.otp import OTP

logger = logging.getLogger(__name__)


class OTPRepositoryImpl(IOTPRepository):
    """Implementación del repositorio OTP usando Django ORM"""
    
    def create(self, email: str, code: str, expired) -> OTP:
        """Crea un nuevo OTP"""
        otp = OTP.objects.create(
            email=email,
            code=code,
            expired=expired
        )
        logger.debug(f"OTP creado para {email}")
        return otp
    
    def find_valid(self, email: str, code: str) -> Optional[OTP]:
        """
        Busca OTP válido
        
        Verifica:
        - Email correcto
        - Código correcto
        - No usado
        - No expirado
        - Intentos disponibles
        """
        try:
            otp = OTP.objects.get(
                email=email,
                code=code,
                is_used=False,
                expired__gt=timezone.now()
            )
            
            if otp.attempts >= 5:
                logger.warning(f"OTP bloqueado por intentos para {email}")
                return None
            
            return otp
            
        except OTP.DoesNotExist:
            logger.debug(f"OTP no encontrado para {email}")
            return None
    
    def invalidate_previous(self, email: str) -> int:
        """Invalida todos los OTPs activos del email"""
        count = OTP.objects.filter(
            email=email,
            is_used=False,
            expired__gt=timezone.now()
        ).update(is_used=True)
        
        if count > 0:
            logger.info(f"Invalidados {count} OTPs anteriores de {email}")
        
        return count
    
    def count_recent(self, email: str, minutes: int = 5) -> int:
        """Cuenta OTPs recientes del email (rate limiting)"""
        cutoff = timezone.now() - timedelta(minutes=minutes)
        return OTP.objects.filter(
            email=email,
            created__gte=cutoff
        ).count()
    
    def delete_expired(self, days: int = 1) -> int:
        """Elimina OTPs expirados antiguos"""
        cutoff = timezone.now() - timedelta(days=days)
        count, _ = OTP.objects.filter(
            expired__lt=cutoff
        ).delete()
        
        if count > 0:
            logger.info(f"Eliminados {count} OTPs expirados")
        
        return count