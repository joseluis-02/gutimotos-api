# Python
import os
import uuid

# Subir imagen al servidor
def get_image_path(instance, filename):
    ext = filename.split('.')[-1]
    unique_id_image = uuid.uuid4().hex
    filename = f"{unique_id_image}.{ext}"
    return os.path.join('motorcycles/', filename)