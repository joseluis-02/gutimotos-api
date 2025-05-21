# Django
from django.db import models

# Modelo para Tipo de documento de identidad para la persona
class IndetityDocumentType(models.Model):
    id = models.PositiveSmallIntegerField(
        null=False,
        blank=False,
        primary_key=True,
        verbose_name="Codigo de sin"
    )
    slug:str = models.SlugField(
        max_length=5,
        null=True,
        blank=True,
        unique=True,
        verbose_name='Abreviatura'
    )
    name:str = models.CharField(
        max_length=120,
        null=False,
        blank= False,
        verbose_name='Tipo documento'
    )
    is_active:bool = models.BooleanField(
        default=True,
        verbose_name='Estado'
    )
    # Manager
    
    # Class Meta
    class Meta:
        pass
    def __str__(self):
        return f'{self.id} {self.name} {self.short_name}'