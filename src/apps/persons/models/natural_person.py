# Django
from django.db import models
from django.core.exceptions import ValidationError
from django.db.models import Q, UniqueConstraint
# Models local
from apps.core.models.base import BasePerson
# Managers
from ..managers import NaturalPersonManager
# Choices
from ..choices import PersonGenderChoices


# Modelo para Persona Natural
class NaturalPerson(BasePerson):
    names:str = models.CharField(
        max_length=50,
        null=False,
        blank=False,
        verbose_name='Nombres',
    )
    paternal_surname:str = models.CharField(
        max_length=50,
        null=False,
        blank=False,
        verbose_name='Apellido paterno',
    )
    maternal_surname:str = models.CharField(
        max_length=50,
        null=False,
        blank=False,
        verbose_name='Apellido materno',
    )
    gender:str = models.CharField(
        max_length=1,
        choices=PersonGenderChoices.choices,
        blank=True,
        default='',
        verbose_name='Género de la persona'
    )
    # Sobreescribimos el atributo de la superclase si es necesario
    '''
    document_code:str = models.CharField(
        max_length=20,
    '''
    document_complement:str = models.CharField(
        max_length=3,
        blank=True,
        default='',
        verbose_name='Complemento de documento',
        help_text='Codigo complemento para documentos duplicados'
    )
    birthdate = models.DateField(
        null=True,
        blank=True,
        verbose_name='Fecha de nacimiento'
    )
    # Manager
    objects = NaturalPersonManager()
    
    # Restricciones de Modelo
    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['document_code', 'document_complement'],
                name='unique_person_document_complement',
            )
        ]
        
    # Validaciones Personalizadas
    def clean(self):
        super().clean()
        # Validación para asegurar que `cedula_identidad` sea única si `codigo_complemento` es null
        if self.document_complement is None:
            if NaturalPerson.objects.filter(
                    document_code=self.document_code,
                    document_complement__exact=''
                ).exclude(id=self.id).exists():
                raise ValidationError("Ya existe una persona natural con esta cédula y sin código de complemento.")
    
    # Mostrar el modelo en formato de texto legible
    def __str__(self):
        return f"{self.names } {self.paternal_surname } {self.maternal_surname }"