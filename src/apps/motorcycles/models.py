# Django
from django.db import models
# django-model-utils
from model_utils.models import TimeStampedModel

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
        erbose_name='Abreviado del país'
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
class Brand(TimeStampedModel):
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
        return self.name

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
    declaration_url:str = models.CharField(
        max_length=250,
        null=True,
        blank=True,
        verbose_name='Declaración en aduana'
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