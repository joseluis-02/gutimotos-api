# Django
from django.db import models
# Modelo Color
class Color(models.Model):
    name:str = models.CharField(
        max_length=50,
        null=False,
        blank=False,
        unique=True,
        verbose_name='Nombre color'
    )
    code_hex:str = models.CharField(
        max_length=6,
        null=True,
        blank=True,
        verbose_name='Código de color'
    )
    class Meta:
        verbose_name = 'Color'
        verbose_name_plural = 'Colores'
        constraints = [
            models.UniqueConstraint(fields=['name','code_hex',], name='unique_color')
        ]
    def __str__(self) -> str:
        return f'{self.name}'