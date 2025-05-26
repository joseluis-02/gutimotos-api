# Django
from django.db import models

class PersonGenderChoices(models.TextChoices):
    MALE:str = 'M','MASCULINO'
    FEMALE:str = 'F','FEMENINO'