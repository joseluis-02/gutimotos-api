# Python
import os
from uuid import uuid4

# Funcion para subir fotos de productos a S3
def upload_to_s3(instance, filename):
    # Obtener el code del producto relacionado
    product_code = str(instance.product.code)
    # Obtener la extensión del archivo
    #ext = os.path.splitext(filename)[1]
    # Generar un nombre único de archivo (opcional, para evitar duplicados)
    filename = f"{uuid4().hex}.webp"
    # Ruta final: products/<product_id>/<archivo>
    return f"fotos/productos/{product_code}/{filename}"