# Python
from uuid import UUID, uuid4
# Django
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
# django-model-utils
from model_utils.models import TimeStampedModel
# Functions
from .functions import get_image_path
# Models
from core.models.natural_or_legal_person import NaturalOrLegalPerson
# Managers
from .managers import MotorcyclePhotoManager
# Choices
from .choices import Orientation, SideDirection

# Modelo Categoría
class Category(TimeStampedModel):
    name:str = models.CharField(
        max_length=70, 
        null=False, 
        verbose_name='Nombre'
    )
    father = models.ForeignKey(
        'self', 
        on_delete=models.CASCADE,
        blank=True, null=True,
        related_name='subcategory', 
        verbose_name='Padre'
    )
    is_active = models.BooleanField(
        default=True, 
        verbose_name='Estado'
    )
    # META
    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'
        # Permite registros únicos
        constraints = [
            models.UniqueConstraint(fields=['name'], name='unique_category')
        ]
    def __str__(self):
        return self.name

    def get_full_path(self):
        url = [self.name]
        father = self.father
        while father is not None:
            url.append(father.name)
            father = father.father
        return " > ".join(url[::-1])

# Modelo Importador
class Importer(NaturalOrLegalPerson,TimeStampedModel):
    is_active:bool = models.BooleanField(
        default=True,
        verbose_name='Estado',
    )
    class Meta:
         pass
    def __str__(self):
        return f'{self.id}'

# Modelo Color
class Color(models.Model):
    name:str = models.CharField(
        max_length=50,
        null=False,
        blank=False,
        unique=True,
        verbose_name='Nombre color'
    )
    code_hex:str = models.CharField(
        max_length=6,
        null=True,
        blank=True,
        verbose_name='Código de color'
    )
    class Meta:
        verbose_name = 'Color'
        verbose_name_plural = 'Colores'
        constraints = [
            models.UniqueConstraint(fields=['name','code_hex',], name='unique_color')
        ]
    def __str__(self) -> str:
        return f'{self.name}'

# Modelo País
class Country(models.Model):
    name:str = models.CharField(
        max_length=100,
        null=False,
        unique=True,
        verbose_name='Nombre del país'
    )
    short_name:str = models.CharField(
        max_length=10,
        null=True,
        unique=True,
        verbose_name='Abreviado del país'
    )
    is_active:bool = models.BooleanField(
        null=False,
        default=True, 
        verbose_name='Estado'
    )
    class Meta:
        verbose_name = 'País'
        verbose_name_plural = 'Paises'
        constraints = [
            models.UniqueConstraint(fields=['name','short_name'], name='unique_country')
        ]
    def __str__(self):
        return f"{self.name}"

# Modelo Marca
class Brand(models.Model):
    name:str = models.CharField(
        max_length=30,
        null=False,
        verbose_name='Nombre marca'
    )
    is_active:bool = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Marca'
        verbose_name_plural = 'Marcas'
        # Permite registros unicos
        constraints = [
            models.UniqueConstraint(fields=['name',], name='unique_brand')
        ]

    def __str__(self):
        return self.name

# Modelo Tipo motocicleta
class MotorcycleType(models.Model):
    name:str = models.CharField(
        max_length=20, 
        null=False, 
        verbose_name='Tipo motocicleta'
    )
    father = models.ForeignKey(
        'self',
        on_delete=models.CASCADE, 
        blank=True, 
        null=True, 
        related_name='subtype', 
        verbose_name='Tipo'
    )
    is_active:bool = models.BooleanField(
        default=True, 
        verbose_name='Estado'
    )
    # META
    class Meta:
        verbose_name = 'Tipo motocicleta'
        verbose_name_plural = 'Tipos de motocicletas'
        constraints = [
            models.UniqueConstraint(fields=['name','father'], name='unique_motorcycle_type')
        ]
        
    def __str__(self):
        return self.get_full_path()

    def get_full_path(self):
        url = [self.name]
        father = self.father
        while father is not None:
            url.append(father.name)
            father = father.father
        return " ".join(url[::-1])

# Modelo Tipo transmision
class TransmissionType(models.Model):
    name:str = models.CharField(
        max_length=70,
        null=False,
        blank=False,
        unique=True,
        verbose_name='Tipo transmisión'
    )
    is_active: bool = models.BooleanField(
        default=True
    )
    def __str__(self):
        return f'{self.name}'

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
        max_length=70,
        null=True,
        blank=True,
        verbose_name='Declaración code',
        help_text='Ingrese el código de declaración de QR'
    )

    # Llaves foráneas
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
    # Muchos a muchos
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
    importer = models.ForeignKey(
        Importer,
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        # Acceso desde Category
        related_name = 'm_importers',
        # Filtro de consultas inversas
        related_query_name='m_importer',
        # Texto de ayuda para el campo
        help_text='Importador de la motocicleta',
        verbose_name='Importador',
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

# Modelo Tipo precio
class TypePrice(models.Model):
    name:str = models.CharField(
        max_length=70,
        null=False,
        blank=False,
    )
    is_active:bool = models.BooleanField(
        default=True
    )

# Modelo Divisa
class Currency(TimeStampedModel):
    # Código de la moneda
    code = models.CharField(
        max_length=3, 
        unique=True, 
        help_text="Código ISO 4217 de la moneda (USD, EUR, CLP, etc.)"
    )
    # Nombre completo de la moneda
    name:str = models.CharField(
        max_length=30,
        null=False,
        blank=False
    )
    # Información de conversión
    conversion_rate = models.DecimalField(
        max_digits=10, 
        decimal_places=4,
        validators=[MinValueValidator(0)],
        help_text="Tasa de cambio respecto a la moneda base"
    )
    is_active:bool = models.BooleanField(
        default=True
    )

# Modelo Precio motocicleta
class MotorcyclePrice(models.Model):
    amount = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(99999.99)
        ]
    )
    description:str = models.CharField(
        max_length=120,
        null=True,
        blank=True,
        verbose_name='Descripción'
    )
    start_date = models.DateField(
        null=False,
        blank=False
    )
    end_date = models.DateField(
        null=True,
        blank=True
    )
    # LLaves externas
    motorcycle_type = models.ForeignKey(
        MotorcycleType,
        null=False,
        blank=False,
        on_delete=models.CASCADE, 
        related_name='mp_motorcycle_types',
        related_query_name='mp_motorcycle_type',
        verbose_name='Tipo motocicleta'
    )
    type_price = models.ForeignKey(
        TypePrice,
        null=False,
        blank=False,
        on_delete=models.CASCADE, 
        related_name='mp_type_prices',
        related_query_name='mp_type_price',
        verbose_name='Tipo precio'
    )
    currency = models.ForeignKey(
        Currency,
        null=False,
        blank=False,
        on_delete=models.CASCADE, 
        related_name='mp_currencies',
        related_query_name='mp_currency',
        verbose_name='Motocicleta'
    )
    is_active:bool = models.BooleanField(
        default=True
    )
    def __str__(self):
        return f'{self.amount} {self.description}'

# Modelo Fotos de la motocicletas
class MotorcyclePhoto(TimeStampedModel):
    orientation:str = models.CharField(
        max_length=1,
        choices=Orientation.choices,
        null=False,
        verbose_name='Orientación de la foto'
    )
    side_direction:str = models.CharField(
        max_length=1,
        choices=SideDirection.choices,
        null=False,
        verbose_name='Dirección de lado'
    )
    image_url = models.ImageField(
        upload_to=get_image_path, 
        blank=False, 
        null=False,
        verbose_name='Foto'
    )
    # Foreing key
    motorcycle_type = models.ForeignKey(
        MotorcycleType, 
        on_delete=models.CASCADE,
        # Acceso desde Motorcycle
        related_name = 'pm_motorcycle_types',
        # Filtro de consultas inversas
        related_query_name='pm_motorcycle_type',
        # Texto de ayuda para el campo
        help_text='Tipo de la motocicleta',
        verbose_name='Tipo',
    )
    color = models.ForeignKey(
        Color, 
        on_delete=models.CASCADE,
        # Acceso desde Motorcycle
        related_name = 'pm_colors',
        # Filtro de consultas inversas
        related_query_name='pm_color',
        # Texto de ayuda para el campo
        help_text='Color del tipo de la motocicleta',
        verbose_name='Color',
    )
    # Manager
    objects = MotorcyclePhotoManager()
    # Class Meta
    class Meta:
        verbose_name = 'Foto de motocicleta'
        verbose_name_plural = 'Fotos de motocicletas'
        constraints = [
            # Asegurar solo una imagen por lado (frontal, trasera, etc.) por tipo y color
            models.UniqueConstraint(
                fields=['motorcycle_type', 'color', 'side_direction'],
                condition=~models.Q(side_direction=SideDirection.PORTADA),
                name='unique_motorcycle_photo_by_type_color_side'
            ),
            models.UniqueConstraint(
                fields=['motorcycle_type', 'color', 'orientation'], 
                condition=models.Q(side_direction=SideDirection.PORTADA),
                name='unique_cover_by_orientation'
            )
        ]
    # Funciones y sobreescritura
    def __str__(self):
        return f'{self.orientation} {self.side_direction} {self.motorcycle_type}'
