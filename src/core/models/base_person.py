# Python
from uuid import UUID, uuid4

from django.db import models


# Modelo abstracto Persona Base
class BasePerson(models.Model):
    id:UUID = models.UUIDField(
        primary_key=True,
        null=False,
        blank=False,
        default=uuid4,
        editable=False
    )
    # Clave foránea de Tipo documento
    document_type: int = models.ForeignKey(
        to='persons.DocumentType',
        # Define el comportamiento cuando se elimina el objeto referenciado
        on_delete=models.SET_NULL,
        # Nombre para acceder a los Tipos Documentos desde el modelo `Perosona Natural`
        related_name='%(class)s_persons',
        # Nombre para acceder al atributo
        related_query_name='%(class)s_person',
        # Permite valores `NULL` en la clave foránea (Tipo Documento opcional)
        null=True,
        # Permite dejar el campo vacío en formularios
        blank=True,
        # Nombre amigable en formularios y el administrador
        verbose_name='Tipo de documento',
        # Texto de ayuda en formularios
        help_text='Selecciona el tipo de documento'
    )
    document_code:str = models.CharField(
        max_length=30,
        blank=True,
        null=True,
        default='',
        verbose_name='Codigo de documento'
    )
    class Meta:
        abstract = True