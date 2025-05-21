# Python
import os
import uuid

# Subir imagen al servidor
def upload_to_s3(instance, filename):
    #ext = filename.split('.')[-1]
    #unique_id_image = uuid.uuid4().hex
    #filename = f"{unique_id_image}.{ext}"
    #return os.path.join('motorcycles/', filename)
    # Obtener el code del producto relacionado
    motorcycle_type = str(instance.motorcycle_type.name)
    color_name = str(instance.color.name)
    # Obtener la extensión del archivo
    ext = os.path.splitext(filename)[1]
    # Generar un nombre único de archivo (opcional, para evitar duplicados)
    filename = f"{uuid.uuid4()}{ext}"
    # Ruta final: products/<product_id>/<archivo>
    return f"motorcycles/{motorcycle_type}/{color_name}/{filename}"