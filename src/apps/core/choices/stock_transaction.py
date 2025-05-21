# Django
from django.db import models

class StockTransaction(models.IntegerChoices):
    ENTRY:bool = True,'Entrada'
    EXIT:bool = False,'Salida'