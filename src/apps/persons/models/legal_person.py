# Django
from django.db import models
from django.core.exceptions import ValidationError
from django.db.models import Q, UniqueConstraint
# Models local
from apps.core.models.base import BasePerson

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