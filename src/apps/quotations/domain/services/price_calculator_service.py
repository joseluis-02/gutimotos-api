# Python
from decimal import Decimal
from typing import Tuple


class PriceCalculatorService:
    """Servicio de dominio para cálculo de precios con margen de ganancia"""
    
    @staticmethod
    def calculate_unit_price(base_price: Decimal, profit_margin: Decimal) -> Decimal:
        """
        Calcula el precio unitario aplicando el margen de ganancia
        
        Args:
            base_price: Precio base del producto
            profit_margin: Margen de ganancia en porcentaje (ej: 10.00 para 10%)
            
        Returns:
            Precio unitario con margen aplicado
        """
        if base_price < 0:
            raise ValueError("El precio base no puede ser negativo")
        if profit_margin < 0:
            raise ValueError("El margen de ganancia no puede ser negativo")
        
        margin_multiplier = Decimal('1') + (profit_margin / Decimal('100'))
        unit_price = base_price * margin_multiplier
        
        # Redondear a 2 decimales
        return unit_price.quantize(Decimal('0.01'))
    
    @staticmethod
    def calculate_item_subtotal(unit_price: Decimal, quantity: int) -> Decimal:
        """
        Calcula el subtotal de un item
        
        Args:
            unit_price: Precio unitario
            quantity: Cantidad
            
        Returns:
            Subtotal del item
        """
        if quantity <= 0:
            raise ValueError("La cantidad debe ser mayor que cero")
        if unit_price < 0:
            raise ValueError("El precio unitario no puede ser negativo")
        
        subtotal = unit_price * Decimal(quantity)
        return subtotal.quantize(Decimal('0.01'))
    
    @staticmethod
    def calculate_quotation_totals(items_subtotals: list[Decimal]) -> Tuple[Decimal, Decimal]:
        """
        Calcula los totales de una cotización
        
        Args:
            items_subtotals: Lista de subtotales de los items
            
        Returns:
            Tupla (subtotal, total) de la cotización
        """
        if not items_subtotals:
            return Decimal('0.00'), Decimal('0.00')
        
        subtotal = sum(items_subtotals, Decimal('0.00'))
        # Por ahora subtotal y total son iguales (sin impuestos)
        total = subtotal
        
        return subtotal.quantize(Decimal('0.01')), total.quantize(Decimal('0.01'))