# Python
from abc import ABC, abstractmethod
from typing import Optional
from datetime import datetime


class IOTPRepository(ABC):
    """
    Interfaz del repositorio OTP
    
    Define el contrato para operaciones con OTPs.
    """
    
    @abstractmethod
    def create(self, email: str, code: str, expired: datetime):
        """Crea un nuevo OTP"""
        pass
    
    @abstractmethod
    def find_valid(self, email: str, code: str):
        """Busca OTP válido por email y código"""
        pass
    
    @abstractmethod
    def invalidate_previous(self, email: str) -> int:
        """Invalida OTPs anteriores del email"""
        pass
    
    @abstractmethod
    def count_recent(self, email: str, minutes: int) -> int:
        """Cuenta OTPs recientes del email"""
        pass
    
    @abstractmethod
    def delete_expired(self, days: int) -> int:
        """Elimina OTPs expirados antiguos"""
        pass