# Django
from django.db import models
# Models
from apps.persons.models import NaturalPerson
from ..models import User
# Modelo Perfil de usuario
class UserProfile(models.Model):
    natural_person = models.OneToOneField(
        NaturalPerson,
        on_delete=models.CASCADE,
        related_name='up_natural_person',
        null=False,
        blank=False,
        verbose_name="Persona asociada"
    )
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='up_user',
        null=False,
        blank=False,
        verbose_name="Usuario asociada"
    )
    # foto de perfil
    def __str__(self):
        return f'{self.natural_person} {self.user}'