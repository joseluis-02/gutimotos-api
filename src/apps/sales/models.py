# Python
import uuid
# Django
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
# Model utils
from model_utils.models import TimeStampedModel
# Models
from apps.customers.models import Customer
from apps.employees.models import Employee
from apps.warehouses.models import Branch
from apps.warehouses.models import MotorcycleInventory

# Modelo Venta
class Sale(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    customer = models.ForeignKey(
        Customer, 
        on_delete=models.PROTECT
    )
    employee = models.ForeignKey(
        Employee, 
        on_delete=models.PROTECT
    )
    branch = models.ForeignKey(
        Branch, 
        on_delete=models.PROTECT
    )
    sale_date = models.DateTimeField(
        auto_now_add=True
    )
    total_sale = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        validators=[
            MinValueValidator(0)
        ]
    )
    def __str__(self):
        return f'{self.customer} {self.employee} {self.branch} {self.sale_date}'

# Modelo Numero venta de la motocicleta
class SaleNumber(models.Model):
    sale = models.ForeignKey(
        Sale,
        on_delete=models.CASCADE,
        related_name='sn_sale'
    )
    motorcycle_inventory = models.OneToOneField(
        MotorcycleInventory,
        on_delete=models.PROTECT,
        related_name='sn_motorcycle_inventory'
    )
    final_price = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(99999.99)
        ]
    )
    def __str__(self):
        return f'{self.sale} {self.motorcycle_inventory}'
