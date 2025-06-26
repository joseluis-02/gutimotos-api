# Django
from django.db import models
# Modelo Tipo transmision
class MotorcycleClass(models.Model):
    slug = models.SlugField(
        unique=True,
        null=False,
        blank=False,
        verbose_name='Slug de la clase de la motocicleta'
    )
    name:str = models.CharField(
        max_length=70,
        null=False,
        blank=False,
        unique=True,
        verbose_name='Clase de motocicleta'
    )
    is_active: bool = models.BooleanField(
        default=True
    )
    class Meta:
        verbose_name = 'Clase motocicleta'
        verbose_name_plural = 'Clases de motocicleta'
    def __str__(self):
        return f'{self.name}'