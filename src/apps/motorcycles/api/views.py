# Django
from django_filters.rest_framework import DjangoFilterBackend
# Django rest-framework
from rest_framework.response import Response
from rest_framework import viewsets, filters
from rest_framework.decorators import action
# Django filters paquete externo
from django_filters.rest_framework import DjangoFilterBackend
# Models
from apps.motorcycles.models import Brand, MotorcyclePhoto
# Serializers
from .serializers import BrandSerializer, MotorcyclePhotoSerializer, MotorcyclePhotoMinimalSerializer
# Paginations
from .paginations import MotorcyclePhotoCustomCursorPagination

# Vista del modelo Brand=Marca GRUD completo
class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    
# Vista de solo lectura para cargar fotos de las motocicletas
class MotorcyclePhotoViewSet(viewsets.ModelViewSet):
    """
    CRUD de fotos de motocicletas con filtros optimizados.
    """
    queryset = MotorcyclePhoto.objects.all()
    serializer_class = MotorcyclePhotoSerializer
    pagination_class = MotorcyclePhotoCustomCursorPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['motorcycle_type', 'color', 'side_direction', 'orientation']
    search_fields = ['motorcycle_type__name', 'color__name']
    ordering_fields = ['created']
    # Por defecto descendente
    ordering = ['-created']
    # Sobreescribiendo el método queryset
    def get_queryset(self):
        queryset = super().get_queryset()
        ordering = self.request.query_params.get('ordering')
        if ordering == 'asc':
            print('ascendente')
            return queryset.order_by('created')
        elif ordering == 'desc':
            print('descendente')
            return queryset.order_by('-created')
        return queryset

    # Sobreescribiendo el método serializer_class
    def get_serializer_class(self):
        """ Usa el serializador simple para listas y el completo para detalles """
        if self.action == 'list':
            return MotorcyclePhotoMinimalSerializer
        return MotorcyclePhotoSerializer
