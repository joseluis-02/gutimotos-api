# Django
from django.db import models
# Apps de terceros -> Model utils
from model_utils.models import TimeStampedModel
# Models local
from apps.persons.models import NaturalPerson
from apps.motorcycles.models import Motorcycle

# Model Accionista=shareholders
class Shareholder(TimeStampedModel):
    is_active:bool = models.BooleanField(
        default=True,
        verbose_name='Estado'
    )
    # Asociamos con una persona natural
    natural_person = models.OneToOneField(
        NaturalPerson,
        on_delete=models.CASCADE,
        related_name='shareholder',
        null=False,
        blank=False,
        verbose_name="Persona asociada"
    )
    # Relacion de muchos a muchos
    motorcycle = models.ManyToManyField(
        Motorcycle,
        blank=True,
        related_name='sh_motorcycles',
        related_query_name='sh_motorcycle',
        verbose_name='Motocicletas',
        help_text='Motocicletas del accionista'
    )
    class Meta:
        verbose_name = 'Accionista'
        verbose_name_plural = 'Accionistas'