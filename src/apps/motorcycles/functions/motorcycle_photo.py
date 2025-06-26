# Python
import os
import uuid

# Subir imagen al servidor
def upload_to_s3(instance, filename):
    motorcycle_type = str(instance.motorcycle_file.motorcycle_type.name)
    brand = str(instance.motorcycle_file.brand.name)
    color_name = str(instance.motorcycle_file.color.name)
    filename = f"{uuid.uuid4().hex}.webp"
    return f"fotos/motocicletas/{brand}/{motorcycle_type}/{color_name}/{filename}"