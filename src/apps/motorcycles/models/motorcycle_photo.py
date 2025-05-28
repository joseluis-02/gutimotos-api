# Django
from django.db import models
# Models utils
from model_utils.models import TimeStampedModel
# Models
from apps.core.models import Color, Brand
from .motorcycle_type import MotorcycleType
# Managers
from ..managers import MotorcyclePhotoManager
# Choices
from ..choices import Orientation, SideDirection
# Functions
from ..functions import upload_to_s3
from apps.core.utils import compress_image_to_webp

# Modelo Fotos de la motocicletas
class MotorcyclePhoto(TimeStampedModel):
    orientation:str = models.CharField(
        max_length=1,
        choices=Orientation.choices,
        null=False,
        verbose_name='Orientación de la foto'
    )
    side_direction:str = models.CharField(
        max_length=1,
        choices=SideDirection.choices,
        null=False,
        verbose_name='Dirección de lado'
    )
    image_url = models.ImageField(
        upload_to=upload_to_s3, 
        blank=False, 
        null=False,
        verbose_name='Foto'
    )
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
    objects = MotorcyclePhotoManager()
    # Class Meta
    class Meta:
        verbose_name = 'Foto de motocicleta'
        verbose_name_plural = 'Fotos de motocicletas'
        constraints = [
            # Asegurar solo una imagen por lado (frontal, trasera, etc.) por tipo y color
            models.UniqueConstraint(
                fields=['motorcycle_type', 'color', 'side_direction'],
                condition=~models.Q(side_direction=SideDirection.PORTADA),
                name='unique_motorcycle_photo_by_type_color_side'
            ),
            models.UniqueConstraint(
                fields=['motorcycle_type', 'color', 'orientation'], 
                condition=models.Q(side_direction=SideDirection.PORTADA),
                name='unique_cover_by_orientation'
            )
        ]
        indexes = [
            models.Index(fields=['created']),
        ]
    # Funciones y sobreescritura
    def __str__(self):
        return f'{self.orientation} {self.side_direction} {self.motorcycle_type}'
    def save(self, *args, **kwargs):
        if self.image_url and not self.image_url.name.endswith(".webp"):
            self.image_url = compress_image_to_webp(self.image_url)

        super().save(*args, **kwargs)