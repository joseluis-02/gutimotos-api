# Django
from django.db import models
# Paquete model utils
from model_utils.models import (
    TimeStampedModel
)
# Modelo abstracto
from apps.core.models.base import NaturalOrLegalPerson

# Modelo Proveedor
class Supplier(NaturalOrLegalPerson,TimeStampedModel):
    is_active:bool = models.BooleanField(
        default=True
    )
    class Meta:
        verbose_name = 'Proveedor'
        verbose_name_plural = 'Proveedores'
    def __str__(self):
        return f'{self.is_active}'
