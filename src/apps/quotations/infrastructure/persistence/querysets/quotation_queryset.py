# Django
from django.db import models
from django.db.models import Prefetch, Q
from django.utils import timezone
# Choices
from apps.quotations.domain.choices.quotation_status import QuotationStatus


class QuotationQuerySet(models.QuerySet):
    """QuerySet personalizado para Quotation"""
    
    def active(self):
        """Cotizaciones activas (no canceladas ni expiradas)"""
        return self.exclude(
            status__in=[QuotationStatus.CANCELLED, QuotationStatus.EXPIRED]
        )
    
    def by_user(self, user):
        """Cotizaciones de un usuario"""
        return self.filter(user=user)
    
    def by_status(self, status):
        """Filtra por estado"""
        return self.filter(status=status)
    
    def created(self):
        """Solo creadas"""
        return self.filter(status=QuotationStatus.CREATED)
    
    def reviewed(self):
        """Solo revisadas"""
        return self.filter(status=QuotationStatus.REVIEWED)
    
    def confirmed(self):
        """Solo confirmadas"""
        return self.filter(status=QuotationStatus.CONFIRMED)
    
    def expired_pending(self):
        """Cotizaciones que deberían estar expiradas pero no están marcadas"""
        return self.filter(
            expired__lt=timezone.now()
        ).exclude(
            status=QuotationStatus.EXPIRED
        )
    
    def with_items(self):
        """Prefetch de items optimizado"""
        from apps.quotations.infrastructure.persistence.models import QuotationItem
        return self.prefetch_related(
            Prefetch(
                'items',
                queryset=QuotationItem.objects.select_related('product')
            )
        )
    
    def with_user(self):
        """Select related de user"""
        return self.select_related('user')
    
    def search(self, query):
        """Búsqueda por ID, whatsapp o usuario"""
        return self.filter(
            Q(id__icontains=query) |
            Q(whatsapp__icontains=query) |
            Q(user__email__icontains=query)
        )
    
    def by_date_range(self, start_date, end_date):
        """Filtra por rango de fechas"""
        return self.filter(created__range=[start_date, end_date])