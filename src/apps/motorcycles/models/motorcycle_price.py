# Python
from decimal import Decimal
# Django
from django.db import models
# django-model-utils
from model_utils.models import TimeStampedModel
# Models
from ..models import MotorcycleType
from apps.core.models import Currency
from apps.core.models import Brand
# Managers

# Modelo MortorcyclePrice
class MotorcyclePrice(TimeStampedModel):
    brand = models.ForeignKey(
        Brand,
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name='motorcycle_prices',
        related_query_name='motorcycle_price',
        help_text='Marca de la motocicleta',
        verbose_name='Marca',
    )
    motorcycle_type = models.ForeignKey(
        MotorcycleType,
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name='motorcycle_prices',
        related_query_name='motorcycle_price',
        help_text='Tipo de motocicleta al que pertenece el precio',
        verbose_name='Tipo de motocicleta',
    )
    currency = models.ForeignKey(
        Currency,
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name='motorcycle_prices',
        related_query_name='motorcycle_price',
        help_text='Moneda del precio para el tipo de motocicleta',
        verbose_name='Moneda',
    )
    base:Decimal = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=False,
        blank=False,
        help_text='Precio base del tipo de motocicleta',
        verbose_name='Precio base',
    )
    # Manager
    # Meta
    class Meta:
        verbose_name = 'Precio de motocicleta'
        verbose_name_plural = 'Precio de motocicletas'
        constraints = [
            models.UniqueConstraint(
                fields=['motorcycle_type','brand','currency'],
                name='unique_motorcycle_price'
            ),
        ]
    def __str__(self):
        return f'{self.motorcycle_type} - {self.base}'
