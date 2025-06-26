# Python 
import uuid
# Django
from django.db import models
# Django utils
from model_utils.models import TimeStampedModel
# Models
from apps.categories.models import Category
from apps.core.models import Brand, Country
from apps.measures.models import Measure
# Managers
from ..managers import ProductManager

# Modelo producto
class Product(TimeStampedModel):
    id:uuid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    category = models.ForeignKey(
        Category,
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name='p_categories',
        related_query_name='p_category',
        help_text='Categoría del producto',
        verbose_name='Categoría',
    )
    measure = models.ForeignKey(
        Measure,
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name='p_measures',
        related_query_name='p_measure',
        help_text='Unidad medida del producto',
        verbose_name='Unidad medida',
    )
    brand = models.ForeignKey(
        Brand,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='p_brands',
        related_query_name='p_brand',
        help_text='Marca del producto',
        verbose_name='Marca',
    )
    country = models.ForeignKey(
        Country,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='p_countries',
        related_query_name='p_countrie',
        help_text='Industria del producto',
        verbose_name='Industria',
    )
    code:str = models.CharField(
        max_length=30,
        null=False,
        blank=False,
        unique=True,
        help_text='Código del producto',
        verbose_name='Código del producto',
    )
    description:str = models.TextField(
        null=False,
        blank=False,
        help_text='Descripción del producto',
        verbose_name='Descripción',
    )
    is_active:bool = models.BooleanField(
        default=True,
        null=False,
        blank=False,
        help_text='Estado del producto',
        verbose_name='Estado',
    )
    # Manager
    objects = ProductManager()
    # Meta
    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        constraints = [
            models.UniqueConstraint(fields=['brand', 'code'], name='unique_product'),
        ]
        indexes = [
            models.Index(fields=['created']),
        ]
    def __str__(self):
        return f'{self.code}'