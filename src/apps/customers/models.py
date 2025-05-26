# Python librerías
from uuid import UUID, uuid4
# Django
from django.db import models
# Django Utils
from model_utils.models import (
    TimeStampedModel
)
# local models
from apps.core.models.base import NaturalOrLegalPerson
# Model Customer
class Customer(NaturalOrLegalPerson,TimeStampedModel):
    id:UUID = models.UUIDField(
        primary_key=True,
        null=False,
        blank=False,
        default=uuid4,
        editable=False,
    )
    is_active:bool = models.BooleanField(
        default=True,
        verbose_name='Estado',
    )
    class Meta:
         pass
    def __str__(self):
        return f'{self.id}'