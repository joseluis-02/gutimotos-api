# Django
from django.db import models
from django.core.exceptions import ValidationError
# Models utils
from model_utils.models import TimeStampedModel
# Models
from .motorcycle_file import MotorcycleFile
# Functions
from ..functions import upload_to_s3
from apps.core.utils import compress_image_to_webp

class MotorcyclePhoto(TimeStampedModel):
    motorcycle_file = models.ForeignKey(
        MotorcycleFile, 
        on_delete=models.CASCADE,
        # Acceso desde Motorcycle
        related_name = 'p_motorcycle_files',
        # Filtro de consultas inversas
        related_query_name='p_motorcycle_file',
        # Texto de ayuda para el campo
        help_text='Archivo de la motocicleta',
        verbose_name='Motocicleta',
    )
    photo = models.ImageField(
        upload_to=upload_to_s3, 
        blank=False, 
        null=False,
        verbose_name='Foto'
    )
    class Meta:
        verbose_name = 'Foto de motocicleta'
        verbose_name_plural = 'Fotos de motocicleta'
        indexes = [
            models.Index(fields=['created']),
        ]
    def save(self, *args, **kwargs):
        try:
            if self.photo and not self.photo.name.endswith('.webp'):
                # Eliminar imagen previa
                if self.pk:
                    try:
                        old = MotorcyclePhoto.objects.get(pk=self.pk)
                        if old.photo and old.photo.name != self.photo.name:
                            old.photo.delete(save=False)
                    except MotorcyclePhoto.DoesNotExist:
                        pass

                # Nombre único
                #unique_filename = f"products/{self.product.code}/{uuid.uuid4().hex}.webp"
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