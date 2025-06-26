# Django
from django.db import models
# Models
from apps.core.models import Color, Brand
from .motorcycle_type import MotorcycleType
# Managers
from ..managers import MotorcycleFileManager


# Modelo Archivo de la motocicletas
class MotorcycleFile(models.Model):
    # Foreing key
    brand = models.ForeignKey(
        Brand, 
        on_delete=models.CASCADE,
        # Acceso desde Motorcycle
        related_name = 'pm_brands',
        # Filtro de consultas inversas
        related_query_name='pm_brand',
        # Texto de ayuda para el campo
        help_text='Marca de la motocicleta',
        verbose_name='Marca',
    )
    motorcycle_type = models.ForeignKey(
        MotorcycleType, 
        on_delete=models.CASCADE,
        # Acceso desde Motorcycle
        related_name = 'pm_motorcycle_types',
        # Filtro de consultas inversas
        related_query_name='pm_motorcycle_type',
        # Texto de ayuda para el campo
        help_text='Tipo de la motocicleta',
        verbose_name='Tipo',
    )
    color = models.ForeignKey(
        Color, 
        on_delete=models.CASCADE,
        # Acceso desde Motorcycle
        related_name = 'pm_colors',
        # Filtro de consultas inversas
        related_query_name='pm_color',
        # Texto de ayuda para el campo
        help_text='Color del tipo de la motocicleta',
        verbose_name='Color',
    )
    # Manager
    objects = MotorcycleFileManager()
    # Class Meta
    class Meta:
        verbose_name = 'Archivo de motocicleta'
        verbose_name_plural = 'Archivos de motocicleta'
        constraints = [
            # Asegurar solo una imagen por lado (frontal, trasera, etc.) por tipo y color
            models.UniqueConstraint(
                fields=['motorcycle_type', 'color', 'brand'],
                name='unique_motorcycle_photo'
            ),
        ]
    # Funciones y sobreescritura
    def __str__(self):
        return f'{self.motorcycle_type} {self.brand.name} {self.color.name}'
   