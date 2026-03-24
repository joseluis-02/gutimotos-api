# quotations/infrastructure/persistence/repositories.py

from typing import Optional
from decimal import Decimal
from uuid import UUID


class DjangoProductRepository:
    """Implementación del repositorio de productos usando Django ORM"""
    
    def find_by_code(self, code: str):
        """Busca un producto activo por su código"""
        from apps.products.models.product import Product
        
        try:
            return Product.objects.select_related().get(
                code=code,
                is_active=True
            )
        except Product.DoesNotExist:
            return None
    
    def get_price(self, product_id: UUID, currency_code: str) -> Optional[Decimal]:
        """Obtiene el precio base de un producto en una moneda específica"""
        from apps.products.models.product_price import ProductPrice
        
        try:
            product_price = ProductPrice.objects.select_related('currency').get(
                product_id=product_id,
                currency__code=currency_code,
                currency__is_active=True
            )
            return product_price.base
        except ProductPrice.DoesNotExist:
            return None


class DjangoTypePriceRepository:
    """Implementación del repositorio de tipos de precio usando Django ORM"""
    
    def find_by_slug(self, slug: str):
        """Busca un tipo de precio por su slug"""
        from apps.core.models.type_price import TypePrice
        
        try:
            return TypePrice.objects.get(slug=slug)
        except TypePrice.DoesNotExist:
            return None


class DjangoCurrencyRepository:
    """Implementación del repositorio de monedas usando Django ORM"""
    
    def find_by_code(self, code: str):
        """Busca una moneda activa por su código"""
        from apps.core.models.currency import Currency
        
        try:
            return Currency.objects.get(code=code, is_active=True)
        except Currency.DoesNotExist:
            return None


class DjangoQuotationRepository:
    """Implementación del repositorio de cotizaciones usando Django ORM"""
    
    def save(self, quotation):
        """Guarda una cotización"""
        quotation.save()
        return quotation
    def find_by_id(self, quotation_id: UUID):
        """Busca una cotización por su ID"""
        from apps.quotations.infrastructure.persistence.models.quotation import Quotation
        try:
            return Quotation.objects.get(id=quotation_id)
        except Quotation.DoesNotExist:
            return None
    def delete_items(self, quotation):
        """Elimina todos los items de una cotización"""
        quotation.items.all().delete()