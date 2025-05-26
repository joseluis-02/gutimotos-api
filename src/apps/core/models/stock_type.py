# Django
from django.db import models
# Choice
from ..choices.stock_transaction import StockTransaction

# Model StockType
class StockType(models.Model):
    slug = models.SlugField(
        max_length=30, 
        unique=True
    ) # Ej: 'facturado', 'sin_factura', 'comision'
    name = models.CharField(
        max_length=70
    ) # Ej: 'Con factura', 'Sin factura', 'En comisión'
    stock_transaction = models.BooleanField(
        choices=StockTransaction,
        default=True,
        verbose_name="¿Es entrada?",
        help_text="Indica si el tipo de stock representa una entrada o una salida"
    )
    is_active = models.BooleanField(default=True)
    class Meta:
        verbose_name = "Tipo de stock"
        verbose_name_plural = "Tipos de stock"
        constraints = [
            models.UniqueConstraint(
                fields=['slug', 'stock_transaction'], 
                name='unique_stock_type'
            ),
        ]
    def __str__(self):
        return f'{self.name} - {"Entrada" if self.stock_transaction else "Salida"}'
