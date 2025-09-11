# Django imports
from django_filters.rest_framework import DjangoFilterBackend
# Django Filters
import django_filters
# Models
from ...models.motorcycle_photo import MotorcyclePhoto

class MotorcyclePhotoFilter(django_filters.FilterSet):
    # Filtros manuales por relación
    brand_id = django_filters.NumberFilter(field_name="motorcycle_file__brand__id")
    color_id = django_filters.NumberFilter(field_name="motorcycle_file__color__id")

    class Meta:
        model = MotorcyclePhoto
        fields = []