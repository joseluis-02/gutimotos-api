# Django
from django.db import models

class PersonGender(models.TextChoices):
    MALE:str = 'M','MASCULINO'
    FEMALE:str = 'F','FEMENINO'

class PersonType(models.TextChoices):
    NATURAL:str = 'n','Persona natural'
    LEGAL:str = 'l','Persona jurídica'