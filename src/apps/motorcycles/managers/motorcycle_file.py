# Django
from django.db import models

# Manager para el modelo MotorcyclePhoto=FotoMotocicleta
class MotorcycleFileManager(models.Manager):
    #def get_queryset(self):
    #    return super().get_queryset().filter(is_active=True)

    def distinct_motorcycle_types_with_colors(self):
        return (
            self.get_queryset()
            .values_list('motorcycle_type__id', flat=True)
            .distinct()
        )