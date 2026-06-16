# Django
from django.db import models
# Querysets
from ..querysets.quotation_queryset import QuotationQuerySet

class QuotationManager(models.Manager):
    """Manager personalizado para Quotation"""
    
    def get_queryset(self):
        return QuotationQuerySet(self.model, using=self._db)
    
    def active(self):
        return self.get_queryset().active()
    
    def by_user(self, user):
        return self.get_queryset().by_user(user)
    
    def by_status(self, status):
        return self.get_queryset().by_status(status)
    
    def created(self):
        return self.get_queryset().created()
    
    def reviewed(self):
        return self.get_queryset().reviewed()
    
    def confirmed(self):
        return self.get_queryset().confirmed()
    
    def expired_pending(self):
        return self.get_queryset().expired_pending()
    
    def with_items(self):
        return self.get_queryset().with_items()
    
    def search(self, query):
        return self.get_queryset().search(query)