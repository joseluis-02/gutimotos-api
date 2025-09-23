# Django
from django.db import models

class ProductType(models.TextChoices):
    MOTORCYCLE:str = 'motorcycle','Motocicleta'
    SPAREPART:str = 'sparepart','Repuesto'
    BOTH:str = 'both','Motocicleta y Repuesto'