# Python
from uuid import uuid4
# Django
from django.db import models
from django.conf import settings
# Managers
from ..managers.quotation_manager import QuotationManager
# Choices
from ....domain.choices.quotation_status import QuotationStatus


class Quotation(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid4,
        editable=False
    )
    # Usuario opcional (cliente autenticado)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        null=False,
        blank=False,
        related_name="quotations"
    )
    created = models.DateTimeField(
        auto_now_add=True
    )
    expired = models.DateTimeField()
    whatsapp = models.CharField(
        max_length=20, 
        null=True, 
        blank=True
    )
    # Snapshot parcial: independiente de cambios futuros
    profit_margin = models.DecimalField(
        max_digits=5, 
        decimal_places=2
    )
    currency_code = models.CharField(
        max_length=3
    )
    # Totales calculados
    subtotal = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        default=0
    )
    total = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        default=0
    )
    # Estado del flujo
    status = models.CharField(
        max_length=20,
        choices=QuotationStatus.choices,
        default=QuotationStatus.CREATED
    )
    notification_sent = models.BooleanField(
        default=False,
        verbose_name='Notificación enviada',
        help_text='Indica si ya se envió notificación de expiración'
    )
    objects = QuotationManager()
    class Meta:
        app_label = 'quotations'
        db_table = 'quotations'
        ordering = ['-created']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['user']),
            models.Index(fields=['created']),
            models.Index(fields=['expired']),
        ]

    def __str__(self):
        return f"Cotización {self.id} - {self.get_status_display()}"

    # Métodos profesionales de dominio
    def set_status(self, new_status: str):
        if new_status not in QuotationStatus.values:
            raise ValueError("Estado inválido para cotización")
        self.status = new_status
        self.save(update_fields=["status"])