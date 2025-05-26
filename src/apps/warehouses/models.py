# Django
from django.db import models
# Paquete model utils
from model_utils.models import (
    TimeStampedModel
)
# Models
from apps.motorcycles.models import Motorcycle
# Choices
from .choices import PhysicalCondition, TransactionStatus

# Model Empresa
class Company(TimeStampedModel):
    foundation_date:str = models.DateField(
        null=False,
        blank=False,
    )
    # Logo
# Modelo Sucursal
class Branch(TimeStampedModel):
    name:str = models.CharField(
        max_length=70,
        null=False,
        blank=False
    )
    company = models.ForeignKey(
        Company, 
        on_delete=models.CASCADE, 
        related_name='branches'
    )
    is_active:bool = models.BooleanField(
        default=True
    )
# Modelo Inventario
class MotorcycleInventory(TimeStampedModel):
    branch = models.ForeignKey(
        Branch,
        on_delete=models.CASCADE,
        verbose_name='Sucursal', 
        related_name='mi_branches'
    )
    motorcycle = models.OneToOneField(
        Motorcycle, 
        verbose_name='Motocicleta', 
        related_name='mi_motorcycles',
        on_delete=models.CASCADE
    )
    physical_condition = models.CharField(
        max_length=2,
        choices=PhysicalCondition.choices,
        null=False,
        blank=False
    )
    transaction_status = models.CharField(
        max_length=2,
        choices=TransactionStatus.choices,
        null=False,
        blank=False
    )
    def __str__(self):
        return f'{self.branch} {self.motorcycle}'