# Django
from django.db import models

class EconomicActivity(models.Model):
    code_sin = models.CharField(
        max_length=10,
        null=False,
        blank=False,
        verbose_name='Código SIN'
    )
    description_sin = models.TextField(
        null=False,
        blank=False,
        verbose_name='Descripción SIN'
    )
    is_primary = models.BooleanField(
        default=False,
        verbose_name='Actividad Primaria'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Estado'
    )

    class Meta:
        verbose_name = 'Actividad Económica'
        verbose_name_plural = 'Actividades Económicas'
        constraints = [
            models.UniqueConstraint(fields=['code_sin'], name='unique_economic_activity')
        ]

    def __str__(self):
        return self.code_sin