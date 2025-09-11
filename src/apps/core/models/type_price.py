# Python
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
import math
# Django
from django.db import models

# TypePrice (Venta, Oferta, Mayorista…)
class TypePrice(models.Model):
    name:str = models.CharField(
        max_length=50,
        null=False,
        blank=False,
        verbose_name="Nombre del tipo de precio",
        help_text="Nombre del tipo de precio, Ej: Precio de venta, Precio de compra"
    )
    slug = models.SlugField(
        unique=True,
        null=False,
        blank=False,
        verbose_name="Slug del tipo de precio",
        help_text="Slug del tipo de precio, Ej: precio-venta, precio-compra"
    )
    profit_margin = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=False,
        blank=False,
        verbose_name="Margen de ganancia producto",
        help_text="Margen de ganancia para productos del tipo de precio, Ej: 10.00"
    )
    profit_margin_motorcycle = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Margen de ganancia motocicleta",
        help_text="Margen de ganancia para motocicletas del tipo de precio, Ej: 5.00"
    )
    is_active:bool = models.BooleanField(
        default=True,
        verbose_name="Tipo de precio activo",
        help_text="Indica si el tipo de precio está activo o no"
    )
    class Meta:
        verbose_name = "Tipo de precio"
        verbose_name_plural = "Tipos de precios"
    def __str__(self):
        return self.name
    # Cálculo progresivo solo para motocicletas
    def calculate_price_motorcycle(self, base_price: Decimal) -> Decimal:
        # Si falta el precio base o el margen -> devolvemos 0
        if base_price is None or self.profit_margin_motorcycle is None:
            return Decimal("0")

        try:
            margen_pct = Decimal(self.profit_margin_motorcycle) / Decimal(100)
            margen_efectivo = margen_pct / Decimal(math.log1p(float(base_price)))
            precio_final = Decimal(base_price) * (Decimal(1) + margen_efectivo)
            
            # Redondear al número entero más cercano
            return precio_final.quantize(Decimal('1'), rounding=ROUND_HALF_UP)
        except (InvalidOperation, ValueError, OverflowError):
            # En caso de error en el cálculo -> devolvemos 0
            return Decimal("0")
    
    def calculate_price_product_scaled_tranches(self, base_price: Decimal) -> Decimal:
        """
        Calcula el precio de un producto aplicando reducción progresiva del profit_margin
        según tramos de 100 unidades de precio.
        """
        if base_price is None or self.profit_margin is None:
            return Decimal("0")
        
        try:
            base_price = Decimal(base_price)
            original_margin = Decimal(self.profit_margin)
            MIN_MARGIN = Decimal("5")  # margen mínimo absoluto

            # Calcular reducción según tramos de 100
            if base_price >= 1000:
                margin = MIN_MARGIN
            else:
                # cantidad de tramos de 100
                tramos = (base_price // 100)
                # reducción 10% por tramo
                reduction_pct = tramos * Decimal("10")
                margin = original_margin * (Decimal("100") - reduction_pct) / Decimal("100")
                margin = max(margin, MIN_MARGIN)

            precio_final = base_price * (Decimal(1) + margin / Decimal(100))
            # devolver número entero
            return precio_final.quantize(Decimal("1"), rounding=ROUND_HALF_UP)

        except Exception:
            return Decimal("0")