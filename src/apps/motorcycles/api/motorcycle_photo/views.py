# Django
from django.db.models import F, Window
from django.db.models.functions import RowNumber
# Django REST Framework
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
# Simple JWT
from rest_framework_simplejwt.authentication import JWTAuthentication
# Models
from ...models.motorcycle_photo import MotorcyclePhoto
# Serializers
from .serializers import MotorcyclePhotoListSerializer, MotorcyclePhotoDetailSerializer, MotorcyclePhotoSerializer
# Paginations
from .paginations import MotorcyclePhotoCursorPagination

class MotorcyclePhotoReadOnlyModelViewSet(viewsets.ReadOnlyModelViewSet):
    authentication_classes = [JWTAuthentication]  # JWT como método de autenticación
    permission_classes = [IsAuthenticated]        # Solo usuarios autenticados
    pagination_class = MotorcyclePhotoCursorPagination
    def get_serializer_class(self):
        if self.action == 'list':
            return MotorcyclePhotoListSerializer
        if self.action == 'retrieve':
            return MotorcyclePhotoDetailSerializer
        return MotorcyclePhotoSerializer

    def get_queryset(self):
        qs = MotorcyclePhoto.objects.all().select_related(
            'motorcycle_file__brand',
            'motorcycle_file__motorcycle_type',
            'motorcycle_file__color',
        )
        if self.action == 'list':
            # Aquí aplicá el filtro para una foto por motorcycle_file, como te mostré antes
            annotated = qs.annotate(
                row_number=Window(
                    expression=RowNumber(),
                    partition_by=[F('motorcycle_file')],
                    order_by=F('created').asc()
                )
            )
            return annotated.filter(row_number=1)
        return qs

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        motorcycle_file = instance.motorcycle_file

        # Obtener todas las fotos de esa motocicleta
        queryset = MotorcyclePhoto.objects.filter(motorcycle_file=motorcycle_file).order_by('-created')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)