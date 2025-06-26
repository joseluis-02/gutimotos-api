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
from ..functions import upload_to_s3
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
    photo:str = models.ImageField(
        upload_to=upload_to_s3,
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
        return f'{self.photo}'
    def save(self, *args, **kwargs):
        try:
            if self.photo and not self.photo.name.endswith('.webp'):
                # Eliminar imagen previa
                if self.pk:
                    try:
                        old = ProductPhoto.objects.get(pk=self.pk)
                        if old.photo and old.photo.name != self.photo.name:
                            old.photo.delete(save=False)
                    except ProductPhoto.DoesNotExist:
                        pass

                # Nombre único
                unique_filename = upload_to_s3
                # Comprimir imagen a ContentFile
                compressed_image = compress_image_to_webp(self.photo, unique_filename)

                # Guardar la imagen comprimida correctamente con el sistema de almacenamiento
                self.photo.save(unique_filename, compressed_image, save=False)

            super().save(*args, **kwargs)

        except ValidationError as ve:
            raise ve
        except Exception as e:
            raise ValidationError(f"No se pudo guardar la imagen: {str(e)}")


    def delete(self, *args, **kwargs):
        if self.photo:
            self.photo.delete(save=False)
        super().delete(*args, **kwargs)