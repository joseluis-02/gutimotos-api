# Python
from decimal import Decimal
# Django
from django.db import models
# django-model-utils
from model_utils.models import TimeStampedModel
# Models
from ..models import Product
from apps.core.models import Currency
# Managers

# Modelo ProductPrice
class ProductPrice(TimeStampedModel):
    product = models.ForeignKey(
        Product,
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name='p_prices',
        related_query_name='p_price',
        help_text='Producto al que pertenece el precio',
        verbose_name='Producto',
    )
    currency = models.ForeignKey(
        Currency,
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name='p_prices',
        related_query_name='p_price',
        help_text='Moneda del precio del producto',
        verbose_name='Moneda',
    )
    base:Decimal = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=False,
        blank=False,
        help_text='Precio base del producto',
        verbose_name='Precio base',
    )
    # Manager
    # Meta
    class Meta:
        verbose_name = 'Precio de producto'
        verbose_name_plural = 'Precios de producto'
        constraints = [
            models.UniqueConstraint(
                fields=['product', 'currency'],
                name='unique_product_price'
            ),
        ]
    def __str__(self):
        return f'{self.product} - {self.base}'
