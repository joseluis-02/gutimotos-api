# Django
from django.db import models
# Modelo Tipo transmision
class TransmissionType(models.Model):
    name:str = models.CharField(
        max_length=70,
        null=False,
        blank=False,
        unique=True,
        verbose_name='Tipo transmisión'
    )
    is_active: bool = models.BooleanField(
        default=True
    )
    class Meta:
        verbose_name = 'Tipo transmisión'
        verbose_name_plural = 'Tipos de transmisión'
    def __str__(self):
        return f'{self.name}'