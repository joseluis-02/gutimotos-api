# Python
import uuid
# Django
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
# Model utils
from model_utils.models import TimeStampedModel
# Models
from apps.warehouses.models import Branch, MotorcycleInventory
from apps.suppliers.models import Supplier

# Modelo Compras
class Purchase(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False
    )
    supplier = models.ForeignKey(
        Supplier, 
        on_delete=models.PROTECT
    )
    branch = models.ForeignKey(
        Branch, 
        on_delete=models.PROTECT
    )
    purchase_date = models.DateTimeField(
        auto_now_add=True
    )
    total_purchase = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        validators=[
            MinValueValidator(0)
        ]
    )
    def __str__(self):
        return f'{self.supplier} {self.branch} {self.purchase_date}'

# Modelo Número de compra de la motocicleta
class PurchaseNumber(models.Model):
    purchase = models.ForeignKey(
        Purchase,
        on_delete=models.CASCADE,
        related_name='pn_purchase'
    )
    motorcycle_inventory = models.OneToOneField(
        MotorcycleInventory,
        on_delete=models.CASCADE,
        related_name='pn_motorcycle_inventory'
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
        return f'{self.purchase} {self.motorcycle_inventory}'
