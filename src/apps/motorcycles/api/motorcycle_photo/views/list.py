from rest_framework import viewsets
from ....models.motorcycle_photo import MotorcyclePhoto
from ..serializers import MotorcyclePhotoMinimalSerializer
from ..filters import MotorcyclePhotoFilter
from django_filters.rest_framework import DjangoFilterBackend
# Paginations
from ..paginations import MotorcyclePhotoCursorPagination

class MotorcyclePhotoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = MotorcyclePhoto.objects.all()
    serializer_class = MotorcyclePhotoMinimalSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = MotorcyclePhotoFilter
    pagination_class = MotorcyclePhotoCursorPagination
