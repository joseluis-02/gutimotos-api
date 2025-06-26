# Python
from uuid import UUID, uuid4
# Django
from django.db import models
# django-model-utils
from model_utils.models import TimeStampedModel
# Models
from apps.categories.models import Category
from apps.core.models import Brand, Color, Country
from .transmission_type import TransmissionType
from .motorcycle_class import MotorcycleClass
from .motorcycle_type import MotorcycleType

# Modelo Motocicleta
class Motorcycle(TimeStampedModel):
    id:UUID = models.UUIDField(
        primary_key=True,
        null=False,
        blank=False,
        default=uuid4,
        editable=False
    )
    code_dim:str = models.CharField(
        max_length=70,
        null=False,
        blank=False,
        unique=True,
        verbose_name='Código DIM'
    )
    code_fvr:str = models.CharField(
        max_length=70,
        null=False,
        blank=False,
        unique=True,
        verbose_name='Código FVR'
    )
    model_year:int = models.PositiveIntegerField(
        null=False,
        blank=False,
        verbose_name='Año modelo'
    )
    manufacturing_year:int = models.PositiveIntegerField(
        null=False,
        blank=False,
        verbose_name='Año fabricación'
    )
    code_chasis:str = models.CharField(
        null=False,
        blank=False,
        unique=True,
        max_length=50,
        verbose_name='Código chasis'
    )
    code_motor:str = models.CharField(
        null=False,
        blank=False,
        unique=True,
        max_length=50,
        verbose_name='Código motor'
    )
    number_cc:int = models.PositiveSmallIntegerField(
        null=False,
        blank=False,
        verbose_name='Número cilindrada'
    )
    declaration_code:str = models.CharField(
        max_length=120,
        null=True,
        blank=True,
        verbose_name='Código de declaración',
        help_text='Ingrese el código de declaración (opcional)'
    )

    # Llaves foráneas
    motorcycle_class:str = models.ForeignKey(
        MotorcycleClass,
        null=False,
        blank=False,
        on_delete=models.CASCADE,
         # Acceso desde ProductType
        related_name = 'm_motorcycle_classes',
        # Filtro de consultas inversas
        related_query_name='m_motorcycle_class',
        # Texto de ayuda para el campo
        help_text='Clase de motocicleta al que pertenece',
        verbose_name='Clase de motocicleta'
    )
    transmission_type:str = models.ForeignKey(
        TransmissionType,
        null=False,
        blank=False,
        on_delete=models.CASCADE,
         # Acceso desde ProductType
        related_name = 'm_transmission_types',
        # Filtro de consultas inversas
        related_query_name='m_transmission_type',
        # Texto de ayuda para el campo
        help_text='Tipo y sub tipo de la motocicleta',
        verbose_name='Tipo de transmisión'
    )
    
    brand = models.ForeignKey(
        Brand,
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        # Acceso desde Brand
        related_name = 'm_brands',
        # Filtro de consultas inversas
        related_query_name='m_brand',
        # Texto de ayuda para el campo
        help_text='Marca de la motocicleta',
        verbose_name='Marca',
    )
    color = models.ForeignKey(
        Color,
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name='m_colors',
        related_query_name='m_color',
        verbose_name='Color',
        help_text='Color de la motocicleta'
    )
    country = models.ForeignKey(
        Country,
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        # Acceso desde Country
        related_name = 'm_countries',
        # Filtro de consultas inversas
        related_query_name='m_country',
        # Texto de ayuda para el campo
        help_text='Origen de la motocicleta',
        verbose_name='Origen',
    )
    
    motorcycle_type = models.ForeignKey(
        MotorcycleType,
        null=False,
        blank=False,
        on_delete=models.CASCADE,
         # Acceso desde ProductType
        related_name = 'm_pmotorcycle_types',
        # Filtro de consultas inversas
        related_query_name='m_motorcycle_type',
        # Texto de ayuda para el campo
        help_text='Tipo de la motocicleta',
        verbose_name='Tipo y subtipo'
    )
    category = models.ForeignKey(
        Category,
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        # Acceso desde Category
        related_name = 'm_categories',
        # Filtro de consultas inversas
        related_query_name='m_category',
        # Texto de ayuda para el campo
        help_text='Categoría de la motocicleta',
        verbose_name='Categoría',
    )
    # Manager

    class Meta:
        verbose_name = 'Motocicleta'
        verbose_name_plural = 'Motocicletas'
        constraints = [
            models.UniqueConstraint(fields=[
                'code_dim',
                'code_chasis',
                'code_motor',
                'code_fvr',
                ], name='unique_motorcycle')
        ]
    def __str__(self) -> str:
        return f'{self.code_dim }'