# Django
from django.db import models
# Choices
from ..choices import CategoryType, CategoryLevel

# Modelo Categoría
class Category(models.Model):
    father = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        blank=True, null=True,
        related_name='subcategory',
        verbose_name='Categoría padre'
    )
    type:str = models.CharField(
        max_length=1,
        choices=CategoryType.choices,
        null=False,
        verbose_name='Tipo de categoría'
    )
    level:str = models.CharField(
        max_length=2,
        choices=CategoryLevel.choices,
        null=False,
        verbose_name='Nivel de categoría'
    )
    code_sin:str = models.CharField(
        max_length=10,
        null=False,
        blank=False,
        verbose_name='Código SIN'
    )
    description_sin:str = models.TextField(
        null=False,
        blank=False,
        verbose_name='Descripción SIN '
    )
    short_description:str = models.CharField(
        max_length=150,
        null=True,
        blank=True,
        verbose_name='Descripción corta'
    )
    is_active:bool = models.BooleanField(
        default=True,
        verbose_name='Estado'
    )
    # META
    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'
        # Permite registros únicos
        constraints = [
            models.UniqueConstraint(fields=['father', 'code_sin'], name='unique_category')
        ]
    def __str__(self):
        return self.code_sin

    def get_full_path(self):
        url = [self.code_sin]
        father = self.father
        while father is not None:
            url.append(father.code_sin)
            father = father.father
        return " > ".join(url[::-1])