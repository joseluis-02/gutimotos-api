# Python
from typing import Optional
from decimal import Decimal
from uuid import UUID
# Django
from django.core.paginator import Paginator

PAGE_SIZE_LIST  = 10   # cotizaciones por página
PAGE_SIZE_ITEMS = 10   # items por página


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
        
    # Lista de cotizaciones del usuario
    def find_by_user(self, user_id: UUID, page: int) -> dict:
        from apps.quotations.infrastructure.persistence.models.quotation import Quotation
 
        qs = (
            Quotation.objects
            .filter(user_id=user_id)
            .only('id', 'status', 'currency_code', 'subtotal', 'total', 'created', 'expired')
            .order_by('-created')
        )
 
        paginator = Paginator(qs, PAGE_SIZE_LIST)
        page_obj  = paginator.get_page(page)
 
        return {
            'results':      list(page_obj.object_list),
            'total_count':  paginator.count,
            'total_pages':  paginator.num_pages,
            'current_page': page_obj.number,
            'has_next':     page_obj.has_next(),
            'has_previous': page_obj.has_previous(),
        }
    
    # Items paginados de una cotización
    def find_items_by_quotation(self, quotation_id: UUID, user_id: UUID, page: int) -> dict:
        from apps.quotations.infrastructure.persistence.models.quotation import Quotation
        from apps.quotations.infrastructure.persistence.models.quotation_item import QuotationItem
 
        # 1. Valida propiedad y trae solo cabecera
        try:
            quotation = (
                Quotation.objects
                #.only('id', 'status', 'currency_code', 'subtotal', 'total')
                .only('id', 'status', 'currency_code', 'subtotal', 'total', 'created', 'expired')
                .get(id=quotation_id, user_id=user_id)
            )
        except Quotation.DoesNotExist:
            return None
 
        # 2. Items con JOIN a producto — sin N+1
        items_qs = (
            QuotationItem.objects
            .filter(quotation_id=quotation_id)
            .select_related('product')
            .only(
                'quantity', 'unit_price', 'subtotal',
                'product__code', 'product__description',
            )
            .order_by('product__code')
        )
 
        paginator = Paginator(items_qs, PAGE_SIZE_ITEMS)
        page_obj  = paginator.get_page(page)
 
        return {
            'quotation':    quotation,
            'items':        list(page_obj.object_list),
            'total_count':  paginator.count,
            'total_pages':  paginator.num_pages,
            'current_page': page_obj.number,
            'has_next':     page_obj.has_next(),
            'has_previous': page_obj.has_previous(),
        }
 