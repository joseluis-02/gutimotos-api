# Django
from django.db import models

# Orientación de la media
class PhysicalCondition(models.TextChoices):
    NO_ARMADO:str = 'NA','NO ARMADO'
    SEMI_ARMADO:str = 'SA','SEMI ARMADO'
    COMPLETAMENTE_ARMADO:str = 'CA','COMPLETAMENTE ARMADO'

class TransactionStatus(models.TextChoices):
    RESERVADA:str = 'RE','RESERVADA'
    DISPONIBLE:str = 'DI','DISPONIBLE'
    VENDIDA:str = 'VE','VENDIDA'