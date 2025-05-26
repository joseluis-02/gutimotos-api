# Django
from django.db import models

# Diferentes tipos de modelos para gestionar precios y tasas de cambio
class Currency(models.Model):
    name:str = models.CharField(
        max_length=50,
        null=False,
        blank=False,
        verbose_name="Nombre de la moneda",
        help_text="Nombre de la moneda, Ej: Dólar, Boliviano, Euro"
    )
    code:str = models.CharField(
        max_length=3, 
        unique=True,
        null=False,
        blank=False,
        verbose_name="Código de la moneda",
        help_text="Código de la moneda, Ej: USD, BOB"
    )
    symbol:str = models.CharField(
        max_length=5,
        null=False,
        blank=False,
        verbose_name="Símbolo de la moneda",
        help_text="Símbolo de la moneda, Ej: $, Bs, €"
    )
    is_active:bool = models.BooleanField(
        default=True,
        verbose_name="Moneda activa",
        help_text="Indica si la moneda está activa o no"
    )
    class Meta:
        verbose_name = "Moneda"
        verbose_name_plural = "Monedas"
        constraints = [
            models.UniqueConstraint(fields=['name', 'code', 'symbol'], name='unique_currency'),
        ]
    def __str__(self):
        return f"{self.name} ({self.code})"