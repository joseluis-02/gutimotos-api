# Python librerías
from uuid import UUID, uuid4
# Django
from django.db import models
from django.core.exceptions import ValidationError
from django.db.models import Q, UniqueConstraint
# Models local
from core.models import BasePerson
# Managers
from .managers import NaturalPersonManager
# Choices local
from core.choices import PersonGender

# Modelo para Tipo de documento de la persona
class DocumentType(models.Model):
    short_name:str = models.CharField(
        max_length=15,
        null=True,
        blank=True,
        verbose_name='Abreviatura'
    )
    name:str = models.CharField(
        max_length=100,
        null=False,
        blank= False,
        verbose_name='Tipo documento'
    )
    is_active:bool = models.BooleanField(
        default=True,
        verbose_name='Estado'
    )
    
    # Include manager
    #objects = DocumentTypeManager()
    # Class Meta
    class Meta:
        pass
    def __str__(self):
        return f'{self.id} {self.name} {self.short_name}'

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
        choices=PersonGender.choices,
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

# Modelo para Persona Jurídica
class LegalPerson(BasePerson):
    company_name:str = models.CharField(
        max_length=70,
        null=False,
        blank=False,
        unique=True,
        verbose_name='Razon social'
    )
    trade_name:str = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name='Nombre comercial'
    )
    # Sobreescribimos de la superclase
    document_code:str = models.CharField(
        max_length=30,
        null=False,
        blank=False,
        unique=True,
        verbose_name='Código de identificación'
    )
    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['company_name', 'document_code'],
                name='unique_company_document_code'
            )
        ]
    def __str__(self):
        return f'{self.company_name} - {self.document_code}'