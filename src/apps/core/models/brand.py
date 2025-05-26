# Django
from django.db import models

# Modelo Marca
class Brand(models.Model):
    name:str = models.CharField(
        max_length=30,
        null=False,
        verbose_name='Nombre marca',
        unique=True,
    )
    is_active:bool = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Marca'
        verbose_name_plural = 'Marcas'
        # Permite registros unicos
        constraints = [
            models.UniqueConstraint(fields=['name',], name='unique_brand_name')
        ]

    def __str__(self):
        return self.name
