# Python
import uuid
# Django
from django.db import models
from django.core.exceptions import ValidationError
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
        try:
            if self.image_url and not self.image_url.name.endswith('.webp'):
                # Eliminar imagen previa
                if self.pk:
                    try:
                        old = ProductPhoto.objects.get(pk=self.pk)
                        if old.image_url and old.image_url.name != self.image_url.name:
                            old.image_url.delete(save=False)
                    except ProductPhoto.DoesNotExist:
                        pass

                # Nombre único
                unique_filename = f"products/{self.product.code}/{uuid.uuid4().hex}.webp"
                
                # Comprimir imagen a ContentFile
                compressed_image = compress_image_to_webp(self.image_url, unique_filename)

                # Guardar la imagen comprimida correctamente con el sistema de almacenamiento
                self.image_url.save(unique_filename, compressed_image, save=False)

            super().save(*args, **kwargs)

        except ValidationError as ve:
            raise ve
        except Exception as e:
            raise ValidationError(f"No se pudo guardar la imagen: {str(e)}")


    def delete(self, *args, **kwargs):
        if self.image_url:
            self.image_url.delete(save=False)
        super().delete(*args, **kwargs)