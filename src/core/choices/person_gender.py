# Django
from django.db import models

class PersonGender(models.TextChoices):
    MALE:str = 'M','MASCULINO'
    FEMALE:str = 'F','FEMENINO'