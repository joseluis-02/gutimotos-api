# Django
from django.db import models

# Modelo País
class Country(models.Model):
    code:str = models.CharField(
        max_length=5,
        null=False,
        unique=True,
        verbose_name='Código de país',
        help_text='Código de país (ej. BOL, BRA, CHI)',
    )
    name:str = models.CharField(
        max_length=70,
        null=False,
        blank=False,
        verbose_name='Nombre del país',
        help_text="Nombre legible del origen (ej. Bolivia, Brasil, China)"
    )
    is_active:bool = models.BooleanField(
        null=False,
        default=True,
        verbose_name='Estado'
    )
    class Meta:
        verbose_name = 'País'
        verbose_name_plural = 'Paises'
        constraints = [
            models.UniqueConstraint(fields=['code','name'], name='unique_country')
        ]
    def __str__(self):
        return f"{self.name}"