# Django
from django.db import models
from django.db.models import Q
# Models
from ..models import Currency
# Managers
from ..managers import ExchangeRateManager

# ExchangeRate sirve para gestionar la conversión entre diferentes monedas
class ExchangeRate(models.Model):
    from_currency = models.ForeignKey(
        Currency,
        on_delete=models.CASCADE,
        related_name="from_rates",
        related_query_name="from_rate",
        verbose_name="Moneda de origen",
        help_text="Moneda de origen, Ej: USD"
    )
    to_currency = models.ForeignKey(
        Currency,
        on_delete=models.CASCADE,
        related_name="to_rates",
        related_query_name="to_rate",
        verbose_name="Moneda de destino",
        help_text="Moneda de destino, Ej: BOB"
    )
    rate = models.DecimalField(
        max_digits=12,
        decimal_places=6,
        null=False,
        blank=False,
        verbose_name="Tasa de cambio",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Fecha de actualización",
        help_text="Fecha de la última actualización de la tasa de cambio"
    )
    is_active:bool = models.BooleanField(
        default=True,
        verbose_name="Tasa de cambio activa",
        help_text="Indica si la tasa de cambio está activa o no"
    )
    # manager
    objects = ExchangeRateManager()
    # Meta
    class Meta:
        verbose_name = "Tasa de cambio"
        verbose_name_plural = "Tasa de cambio"
        constraints = [
            models.UniqueConstraint(
                fields=['from_currency', 'to_currency'],
                name='unique_exchange_rate'
            ),
            models.CheckConstraint(
                check=~Q(from_currency=models.F('to_currency')),
                name='no_same_currency'
            ),
        ]
    def __str__(self):
        return f"{self.from_currency} -> {self.to_currency}: {self.rate}"
