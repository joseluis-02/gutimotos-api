# Django
from django.db import models

# QuerySet para el modelo Product
class ProductQuerySet(models.QuerySet):
    def active(self):
        return self.filter(is_active=True)

    def with_related_light(self):
        return self.select_related('brand', 'country').only(
            'id', 'code', 'description',
            'brand__name', 'country__code', 'measure__name'
        )
