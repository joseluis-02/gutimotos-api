# Python
from uuid import UUID, uuid4

# Django
from django.db import models
from django.db.models import Q
from django.forms import ValidationError

# Choices local
from apps.core.choices import PersonType

'''
Modelo abstracto para indicar que puede pertenecer a una persona natural o juridica
pero no ambos ni vacío 
'''
class NaturalOrLegalPerson(models.Model):
    person_type = models.CharField(
        max_length=1,
        null=False,
        blank=False,
        default=PersonType.NATURAL,
        choices=PersonType.choices,
        verbose_name='Tipo persona',
        help_text='Selecciona el tipo de persona'
    )
    natural_person:UUID = models.ForeignKey(
        to='persons.NaturalPerson',
        null=True,
        blank=True,
        on_delete=models.RESTRICT,
        related_name='%(class)ss_natural_perosn',
        related_query_name='%(class)s_natural_person',
        verbose_name='Persona natural',
        help_text='Selecciona una persona natural',
    )
    legal_person:UUID = models.ForeignKey(
        to='persons.LegalPerson',
        null=True,
        blank=True,
        on_delete=models.RESTRICT,
        related_name='%(class)ss_legal_perosn',
        related_query_name='%(class)s_legal_person',
        verbose_name='Persona jurídica',
        help_text='Selecciona una persona jurídica',
    )
    class Meta:
        abstract = True
        constraints = [
            models.CheckConstraint(
                check=(
                    Q(natural_person__isnull=False, legal_person__isnull=True) | 
                    Q(natural_person__isnull=True, legal_person__isnull=False)
                ),
                name="check_only_one_person"
            )
        ]
    def clean(self):
        super().clean()
        # Validar que solo uno de los campos está definido y no ambos ni ninguno
        if (
            (self.natural_person is None and self.legal_person is None) or 
            (self.natural_person is not None and self.legal_person is not None)
        ):
            raise ValidationError("Debe asociarse a una Persona Natural o una Persona Jurídica, pero no ambas ni ninguna.")
        # Validar que el campo correcto esté lleno según el tipo de persona
        if self.person_type == PersonType.NATURAL and self.natural_person is None:
            raise ValidationError(
                "El tipo seleccionado es 'Persona Natural', pero no se ha proporcionado una persona natural."
            )
        elif self.person_type == PersonType.LEGAL and self.legal_person is None:
            raise ValidationError(
                "El tipo seleccionado es 'Persona Jurídica', pero no se ha proporcionado una persona jurídica."
            )
    def save(self, *args, **kwargs):
        # Llamar a la validación antes de guardar
        self.clean()
        super().save(*args, **kwargs)