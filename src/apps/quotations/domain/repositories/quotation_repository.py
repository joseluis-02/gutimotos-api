# Python
from abc import ABC, abstractmethod
from typing import Optional
from decimal import Decimal
from uuid import UUID


class IProductRepository(ABC):
    """Interfaz para el repositorio de productos"""
    
    @abstractmethod
    def find_by_code(self, code: str):
        """Busca un producto por su código"""
        pass
    
    @abstractmethod
    def get_price(self, product_id: UUID, currency_code: str) -> Optional[Decimal]:
        """Obtiene el precio base de un producto en una moneda específica"""
        pass


class ITypePriceRepository(ABC):
    """Interfaz para el repositorio de tipos de precio"""
    
    @abstractmethod
    def find_by_slug(self, slug: str):
        """Busca un tipo de precio por su slug"""
        pass


class ICurrencyRepository(ABC):
    """Interfaz para el repositorio de monedas"""
    
    @abstractmethod
    def find_by_code(self, code: str):
        """Busca una moneda activa por su código"""
        pass

# Quotation
class IQuotationRepository(ABC):
    """Interfaz para el repositorio de cotizaciones"""
    
    @abstractmethod
    def save(self, quotation):
        """Guarda una cotización"""
        pass
    @abstractmethod
    def find_by_id(self, quotation_id: UUID):
        """Busca una cotización por su ID"""
        pass
    @abstractmethod
    def delete_items(self, quotation):
        """Elimina todos los items de una cotización"""
        pass
    @abstractmethod
    def find_by_user(self, user_id: UUID, page: int) -> dict:
        """Lista cotizaciones de un usuario — 10 registros por página"""
        pass
 
    @abstractmethod
    def find_items_by_quotation(self, quotation_id: UUID, user_id: UUID, page: int) -> dict:
        """Items paginados de una cotización — 50 registros por página"""
        pass