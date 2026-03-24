# Python
from uuid import uuid4
# Django
from django.db import models
from django.core.exceptions import ValidationError
# Models
from .quotation import Quotation
from apps.products.models.product import Product

class QuotationItem(models.Model):
    quotation = models.ForeignKey(
        Quotation,
        related_name="items",
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT
    )
    # Datos esenciales de la cotización
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["quotation", "product"],
                name="uq_quotation_product"
            )
        ]
        indexes = [
            models.Index(fields=["quotation"]),
            models.Index(fields=["product"]),
        ]
        ordering = ["quotation", "product"]

    def __str__(self):
        return f"{self.product.description} x {self.quantity}"

    def clean(self):
        if self.quantity <= 0:
            raise ValidationError("La cantidad debe ser mayor que cero.")
        if self.unit_price < 0:
            raise ValidationError("El precio unitario no puede ser negativo.")

    def save(self, *args, **kwargs):
        # Calcula subtotal automáticamente
        self.subtotal = self.unit_price * self.quantity
        self.full_clean()
        super().save(*args, **kwargs)