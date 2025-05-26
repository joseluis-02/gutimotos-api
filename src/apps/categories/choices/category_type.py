# Django
from django.db import models

# Tipo de la categoría
class CategoryType(models.TextChoices):
    ACTIVIDAD:str = 'A','Actividad'
    PRODUCTO:str = 'p','Producto'