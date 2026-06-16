# Python
from dataclasses import dataclass
from typing import List
from decimal import Decimal
from datetime import datetime
from uuid import UUID


@dataclass(frozen=True)
class QuotationItemRequestDTO:
    """DTO para un item de cotización desde el frontend"""
    product_code: str
    quantity: int

    def __post_init__(self):
        if self.quantity <= 0:
            raise ValueError("La cantidad debe ser mayor que cero")
        if not self.product_code or not self.product_code.strip():
            raise ValueError("El código de producto es requerido")


@dataclass(frozen=True)
class CreateQuotationRequestDTO:
    """DTO para la creación de una cotización"""
    user_id: UUID
    items: List[QuotationItemRequestDTO]
    type_price_slug: str
    currency_code: str
    whatsapp: str | None = None
    
    def __post_init__(self):
        if not self.items:
            raise ValueError("Debe incluir al menos un item en la cotización")
        if not self.type_price_slug:
            raise ValueError("El tipo de precio es requerido")
        if not self.currency_code:
            raise ValueError("El código de moneda es requerido")


@dataclass(frozen=True)
class QuotationItemResponseDTO:
    """DTO para un item de cotización en la respuesta"""
    product_code: str
    product_description: str
    quantity: int
    unit_price: Decimal
    subtotal: Decimal


@dataclass(frozen=True)
class QuotationResponseDTO:
    """DTO para la respuesta de una cotización creada"""
    id: UUID
    user_id: UUID
    created: datetime
    expired: datetime
    whatsapp: str | None
    profit_margin: Decimal
    currency_code: str
    currency_symbol: str
    subtotal: Decimal
    total: Decimal
    status: str
    items: List[QuotationItemResponseDTO]


# Actualizar estado de cotizacion
@dataclass(frozen=True)
class UpdateQuotationStatusRequestDTO:
    """DTO para actualizar estado de cotización"""
    quotation_id: UUID
    new_status: str
    user_id: UUID


@dataclass(frozen=True)
class UpdateQuotationStatusResponseDTO:
    """DTO de respuesta al actualizar estado"""
    quotation_id: UUID
    status: str
    message: str

# Actualizar los items de la cotización.
@dataclass(frozen=True)
class UpdateQuotationItemDTO:
    """DTO para actualizar un item"""
    product_code: str
    quantity: int


@dataclass(frozen=True)
class UpdateQuotationItemsRequestDTO:
    """DTO para actualizar items de cotización"""
    quotation_id: UUID
    user_id: UUID
    items: List[UpdateQuotationItemDTO]


@dataclass(frozen=True)
class UpdateQuotationItemsResponseDTO:
    """DTO de respuesta"""
    quotation_id: UUID
    subtotal: Decimal
    total: Decimal
    items: List[QuotationItemResponseDTO]