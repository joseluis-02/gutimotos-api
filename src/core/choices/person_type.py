# Django
from django.db import models

class PersonType(models.TextChoices):
    NATURAL:str = 'n','Persona natural'
    LEGAL:str = 'l','Persona jurídica'