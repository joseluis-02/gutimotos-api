# Django
from django.db import models
# Choices
from ..choices.product_type import ProductType

# Modelo Marca
class Brand(models.Model):
    name:str = models.CharField(
        max_length=30,
        null=False,
        verbose_name='Nombre marca',
        unique=True,
    )
    product_type = models.CharField(
        max_length=20,
        choices=ProductType.choices,
        default=ProductType.BOTH,
        verbose_name="Tipo de producto",
    )
    is_active:bool = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Marca'
        verbose_name_plural = 'Marcas'

    def __str__(self):
        return self.name
