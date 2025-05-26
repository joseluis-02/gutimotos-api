# Django
from django.db import models
# QuerySets
from ..querysets import ProductQuerySet

class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)

    def active_with_related(self):
        return self.get_queryset().active().with_related_light()
