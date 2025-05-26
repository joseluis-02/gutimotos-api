# Django
from django.db import models
# Models
from .product import Product
from apps.core.models import StockType

# Model ProductStockEntry
class ProductStock(models.Model):
    product = models.ForeignKey(
        Product, 
        on_delete=models.CASCADE, 
        related_name='stock_entries'
    )
    stock_type = models.ForeignKey(
        StockType, 
        on_delete=models.PROTECT, 
        related_name='stock_entries'
    )
    # Branch
    quantity = models.PositiveIntegerField(
        verbose_name='Cantidad',
        help_text='Cantidad de productos para este tipo de movimiento'
    )
    class Meta:
        verbose_name = 'Stock de producto'
        verbose_name_plural = 'Stocks de producto'
        constraints = [
            models.UniqueConstraint(
                fields=['product', 'stock_type'], 
                name='unique_product_stock'
            ),
        ]

    def __str__(self):
        return f'{self.product} - {self.quantity} [{self.stock_type}]'