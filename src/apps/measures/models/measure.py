# Django
from django.db import models

# Modelo Unidad de medida
class Measure(models.Model):
    code_sin:int = models.PositiveSmallIntegerField(
        null=False,
        verbose_name='Código SIN'
    )
    short_name:str = models.CharField(
        max_length=6,
        null=False,
        verbose_name='Abreviatura de la Unidad de Medida'
    )
    name:str = models.CharField(
        max_length=70,
        null=False,
        verbose_name='Descripción de la Unidad de Medida'
    )
    is_active:bool = models.BooleanField(
        default=True,
        verbose_name='Estado'
    )
    # META
    class Meta:
        verbose_name = 'Unidad de Medida'
        verbose_name_plural = 'Unidades de Medida'
        # Permite registros únicos
        constraints = [
            models.UniqueConstraint(fields=['code_sin','short_name', 'name'], name='unique_measure')
        ]
    def __str__(self):
        return self.name