# Django
from django.db import models

# Manager para el modelo MotorcyclePhoto=FotoMotocicleta
class MotorcycleFileManager(models.Manager):
    def distinct_motorcycle_types_with_colors(self):
        return (
            self.get_queryset()
            .values_list(
                'motorcycle_type__id'
            )
            .distinct()
        )