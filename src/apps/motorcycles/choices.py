# Django
from django.db import models

# Orientación de la media
class Orientation(models.TextChoices):
    VERTICAL:str = 'V','Vertical'
    HORIZONTAL:str = 'H','Horizontal'

# Lado dirección
class SideDirection(models.TextChoices):
    PORTADA:str = 'P', 'Portada'
    FRONTAL:str = 'F','Frontal'
    TRASERA:str = 'T','Trasera'
    IZQUIERDA:str = 'I','Izquierda'
    DERECHA:str = 'D','Derecha'