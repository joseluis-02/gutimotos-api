# Python
import uuid
from datetime import timedelta
# Django
from django.db import models
from django.utils import timezone
from django.conf import settings

class OTP(models.Model):
    """
    Modelo para códigos OTP - Autenticación y Verificación
    
    Casos de uso:
    - Login de usuarios verificados (passwordless)
    - Verificación de email de usuarios nuevos
    - Verificación de email de usuarios existentes no verificados
    """
    
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    
    email = models.EmailField(
        db_index=True,
        verbose_name='Email'
    )
    
    code = models.CharField(
        max_length=6,
        verbose_name='Código OTP'
    )
    
    is_used = models.BooleanField(
        default=False,
        db_index=True,
        verbose_name='Usado'
    )
    
    attempts = models.PositiveSmallIntegerField(
        default=0,
        verbose_name='Intentos fallidos'
    )
    
    created = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Creado'
    )
    
    expired = models.DateTimeField(
        db_index=True,
        verbose_name='Expira'
    )
    
    class Meta:
        db_table = 'user_otps'
        ordering = ['-created']
        indexes = [
            models.Index(fields=['email', 'is_used', 'expired']),
            models.Index(fields=['code', 'expired']),
        ]
        verbose_name = 'OTP'
        verbose_name_plural = 'OTPs'
    
    def __str__(self):
        return f"OTP for {self.email}"
    
    def is_valid(self) -> bool:
        """Verifica si el OTP es válido"""
        return (
            not self.is_used and
            timezone.now() < self.expired and
            self.attempts < 5
        )
    
    def mark_as_used(self) -> None:
        """Marca el OTP como usado"""
        self.is_used = True
        self.save(update_fields=['is_used'])
    
    def increment_attempts(self) -> None:
        """Incrementa contador de intentos fallidos"""
        self.attempts += 1
        self.save(update_fields=['attempts'])
    
    @staticmethod
    def get_expiration_time(minutes: int = 10):
        """Calcula tiempo de expiración"""
        return timezone.now() + timedelta(minutes=minutes)