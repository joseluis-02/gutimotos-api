from PIL import Image
import uuid
from django.core.files.base import ContentFile
from io import BytesIO

def compress_image_to_webp(image):
    img = Image.open(image)
    img_io = BytesIO()
    img.save(img_io, format='WEBP', quality=80)
    img_io.seek(0)

    ext = 'webp'
    filename = f"{uuid.uuid4().hex}.{ext}"

    return ContentFile(img_io.read(), name=filename)
