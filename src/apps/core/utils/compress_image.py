# Python
import uuid
import logging
from PIL import Image, UnidentifiedImageError
from io import BytesIO
# Django
from django.core.files.base import ContentFile
from django.core.exceptions import ValidationError
# Logger
logger = logging.getLogger(__name__)

def compress_image_to_webp(image_file, filename, quality=80):
    try:
        img = Image.open(image_file)

        # Validar que sea una imagen
        if img.format not in ['JPEG','JPG', 'PNG', 'WEBP','HEIC']:
            raise ValidationError("Formato de imagen no soportado: solo JPG, PNG o WEBP.")

        # Convertir si tiene transparencia
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")

        img_io = BytesIO()
        img.save(img_io, format='WEBP', quality=quality)
        img_io.seek(0)

        return ContentFile(img_io.read(), name=filename)
    except UnidentifiedImageError:
        logger.error("Archivo no es una imagen válida.")
        raise ValidationError("El archivo proporcionado no es una imagen válida.")
    except Exception as e:
        logger.exception("Error al comprimir imagen")
        raise ValidationError(f"Error al procesar la imagen: {str(e)}")