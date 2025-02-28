# Django
from django.db import models
# Model utils
from model_utils.models import TimeStampedModel
# Models
from apps.persons.models import NaturalPerson

# Modelo Empleado
class Employee(TimeStampedModel):
    is_active:bool = models.BooleanField(
        default=True,
        verbose_name='Estado'
    )
    # Asociamos con una persona natural
    natural_person = models.OneToOneField(
        NaturalPerson,
        on_delete=models.CASCADE,
        related_name='employee',
        null=False,
        blank=False,
        verbose_name="Persona asociada"
    )