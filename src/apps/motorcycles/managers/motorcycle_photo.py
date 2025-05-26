# Django
from django.db import models

# Manager para el modelo MotorcyclePhoto=FotoMotocicleta
class MotorcyclePhotoManager(models.Manager):
    def distinct_motorcycle_types_with_colors(self):
        return (
            self.get_queryset()
            .values_list(
                'motorcycle_type__id',
                'image_url'
            )
            .distinct().order_by('-created')
        )