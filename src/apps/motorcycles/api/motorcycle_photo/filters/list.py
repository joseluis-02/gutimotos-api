from django.db.models.functions import Greatest
from django.contrib.postgres.search import TrigramSimilarity
from django_filters.rest_framework import FilterSet, filters
from ....models.motorcycle_photo import MotorcyclePhoto

class MotorcyclePhotoFilter(FilterSet):
    search = filters.CharFilter(method='filter_search')
    brand = filters.NumberFilter(field_name='brand__id')
    motorcycle_type = filters.NumberFilter(field_name='motorcycle_type__id')
    color = filters.NumberFilter(field_name='color__id')

    class Meta:
        model = MotorcyclePhoto
        fields = ['brand', 'motorcycle_type', 'color', 'orientation', 'side_direction']

    def filter_search(self, queryset, name, value):
        return queryset.annotate(
            sim_brand=TrigramSimilarity('brand__name', value),
            sim_type=TrigramSimilarity('motorcycle_type__name', value),
            sim_color=TrigramSimilarity('color__name', value),
            similarity=Greatest(
                TrigramSimilarity('brand__name', value),
                TrigramSimilarity('motorcycle_type__name', value),
                TrigramSimilarity('color__name', value),
            )
        ).filter(similarity__gt=0.2).order_by('-similarity')
