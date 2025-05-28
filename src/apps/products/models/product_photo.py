# Django
from django.db import models
# Models utils
from model_utils.models import TimeStampedModel
# Models
from ..models import Product
# Functions
from ..functions import product_photo_upload_s3
from apps.core.utils import compress_image_to_webp

# Modelo imagen del producto
class ProductPhoto(TimeStampedModel):
    product = models.ForeignKey(
        Product,
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name='p_photos',
        related_query_name='p_photo',
        help_text='Producto al que pertenece la foto',
        verbose_name='Producto',
    )
    image_url:str = models.ImageField(
        upload_to=product_photo_upload_s3,
        null=False,
        blank=False,
        help_text='Nombre de la foto del producto',
        verbose_name='Foto',
    )
    class Meta:
        verbose_name = 'Foto de producto'
        verbose_name_plural = 'Fotos de producto'
        indexes = [
            models.Index(fields=['created']),
        ]
    def __str__(self):
        return f'{self.image_url}'
    def save(self, *args, **kwargs):
        if self.image_url and not self.image_url.name.endswith(".webp"):
            self.image_url = compress_image_to_webp(self.image_url)

        super().save(*args, **kwargs)