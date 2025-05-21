# Django
from django.db import models

# Nivel de la categoría
class CategoryLevel(models.TextChoices):
    PRINCIPAL:str = 'P', 'Principal'
    SECUNDARIO:str = 'S','Secundario'
    IMPORTADO_MI:str = 'IM','Importado por mi'
    IMPORTADO_OTROS:str = 'IO','Importado por otros'