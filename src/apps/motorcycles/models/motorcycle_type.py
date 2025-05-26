# Django
from django.db import models
from django.core.exceptions import ValidationError

# Modelo Tipo motocicleta
class MotorcycleType(models.Model):
    name = models.CharField(
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
    is_active = models.BooleanField(
        default=True, 
        verbose_name='Estado'
    )
    is_subtype = models.BooleanField(
        default=False,
        verbose_name='Es subtipo',
        help_text='Indica si este es un subtipo de otro tipo de motocicleta'
    )
    class Meta:
        verbose_name = 'Tipo motocicleta'
        verbose_name_plural = 'Tipos de motocicletas'
        constraints = [
            models.UniqueConstraint(fields=['name', 'father'], name='unique_motorcycle_type'),
        ]

    def __str__(self):
        return f'{self.get_full_path()}'

    def get_full_path(self):
        url = [self.name]
        father = self.father
        while father is not None:
            url.append(father.name)
            father = father.father
        return " ".join(url[::-1])

    def clean(self):
        # Evitar consultas innecesarias con exists()
        if self.is_subtype:
            if self.father is None:
                raise ValidationError('Un subtipo debe tener un tipo padre.')
            # Validar si el subtipo con el nombre ya existe para este padre
            if MotorcycleType.objects.filter(name=self.name, father=self.father).exists():
                raise ValidationError(f'Ya existe un subtipo {self.name} bajo el tipo {self.father.name}')
        else:
            if self.father is not None:
                raise ValidationError('Un tipo de motocycleta no debe tener padre.')
            # Validar si el tipo con el nombre ya existe
            if MotorcycleType.objects.filter(name=self.name, father=None).exists():
                raise ValidationError(f'Ya existe un tipo de motocicleta con el nombre {self.name}')

        super().clean()