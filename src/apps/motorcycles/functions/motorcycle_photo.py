# Python
import os
import uuid

# Subir imagen al servidor
def upload_to_s3(instance, filename):
    motorcycle_type = str(instance.motorcycle_type.name)
    color_name = str(instance.color.name)
    # Obtener la extensión del archivo
    ext = os.path.splitext(filename)[1]
    # Generar un nombre único de archivo (opcional, para evitar duplicados)
    filename = f"{uuid.uuid4().hex}.{ext}"
    # Ruta final: products/<product_id>/<archivo>
    return f"motorcycles/{motorcycle_type}/{color_name}/{filename}"