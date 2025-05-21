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
        verbose_name="Margen de ganancia",
        help_text="Margen de ganancia del tipo de precio, Ej: 10.00"
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