# Python
from decimal import Decimal
from typing import List, Dict
from datetime import datetime, timedelta
# Django
from django.utils import timezone
# Choices
from apps.quotations.domain.choices.quotation_status import QuotationStatus


class QuotationCalculator:
    """Servicio de dominio para cálculos de cotización"""
    
    @staticmethod
    def calculate_item_subtotal(quantity: int, unit_price: Decimal) -> Decimal:
        """Calcula subtotal de un item"""
        return Decimal(quantity) * unit_price
    
    @staticmethod
    def calculate_quotation_subtotal(items: List[Dict]) -> Decimal:
        """
        Calcula subtotal de la cotización sumando items
        items: [{'quantity': int, 'unit_price': Decimal}, ...]
        """
        subtotal = Decimal('0.00')
        for item in items:
            subtotal += QuotationCalculator.calculate_item_subtotal(
                item['quantity'],
                item['unit_price']
            )
        return subtotal
    
    @staticmethod
    def calculate_total_with_margin(subtotal: Decimal, profit_margin: Decimal) -> Decimal:
        """
        Calcula total aplicando margen de ganancia
        """
        margin_multiplier = Decimal('1') + (profit_margin / Decimal('100'))
        return subtotal * margin_multiplier
    
    @staticmethod
    def calculate_expiration_date(days: int = 7) -> datetime:
        """Calcula fecha de expiración (por defecto 7 días)"""
        return timezone.now() + timedelta(days=days)


class QuotationValidator:
    """Servicio de dominio para validaciones"""
    
    @staticmethod
    def can_transition_to(current_status: str, new_status: str) -> bool:
        """Valida si puede cambiar de estado"""
        allowed = QuotationStatus.valid_transitions(current_status)
        return new_status in [s.value for s in allowed]
    
    @staticmethod
    def is_expired(expired_date: datetime) -> bool:
        """Verifica si la cotización está expirada"""
        return timezone.now() > expired_date
    
    @staticmethod
    def can_be_modified(status: str) -> bool:
        """Verifica si la cotización puede modificarse"""
        return status in [
            QuotationStatus.CREATED.value,
            QuotationStatus.REVIEWED.value
        ]
    
    @staticmethod
    def can_be_deleted(status: str) -> bool:
        """Verifica si la cotización puede eliminarse"""
        return status == QuotationStatus.CREATED.value