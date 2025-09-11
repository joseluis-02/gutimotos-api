# Django
from django.db.models import F, Window
from django.db.models.functions import RowNumber
from django_filters.rest_framework import DjangoFilterBackend
from django.http import Http404
# Django REST Framework
from rest_framework import viewsets,status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
# Simple JWT
from rest_framework_simplejwt.authentication import JWTAuthentication
# Models
from ...models.motorcycle_photo import MotorcyclePhoto
# Serializers
from .serializers import MotorcyclePhotoListSerializer, MotorcyclePhotoDetailSerializer, MotorcyclePhotoSerializer
# Paginations
from .paginations import MotorcyclePhotoCursorPagination
# filters
from .filters import MotorcyclePhotoFilter
# Mixins
from .mixins import PublicListPrivateRetrieveMixin

class MotorcyclePhotoReadOnlyModelViewSet(viewsets.ReadOnlyModelViewSet):
    #authentication_classes = [JWTAuthentication]
    #permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = MotorcyclePhotoFilter
    pagination_class = MotorcyclePhotoCursorPagination

    def get_authenticators(self):
        """Sólo pedimos autenticación en retrieve"""
        if self.request and self.detail:  # estamos en /<pk>/ → retrieve
            return [JWTAuthentication()]
        return []  # list y demás no usan autenticación

    def get_permissions(self):
        if self.detail:  # retrieve
            return [IsAuthenticated()]
        return [AllowAny()]  # list y demás son públicos

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
            # Aquí aplicá el filtro para una foto por motorcycle_file
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
        try:
            instance = self.get_object()
        except Http404:
            return Response(
                {
                    "success": False,
                    "message": f"No se encontró un registro con ID={kwargs.get('pk')}",
                    "data": None
                },
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            # Para cualquier otro error inesperado
            return Response(
                {
                    "success": False,
                    "message": str(e),
                    "data": None
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        motorcycle_file = instance.motorcycle_file

        # Traer todas las fotos de esa motocicleta de forma eficiente
        queryset = MotorcyclePhoto.objects.filter(
            motorcycle_file=motorcycle_file
        ).select_related(
            'motorcycle_file__motorcycle_type'
        ).order_by('-created')

        serializer = self.get_serializer(queryset, many=True)

        return Response({
            "success": True,
            "message": f"Se ha obtenido las fotos de un tipo de motocicleta con ID:{motorcycle_file.motorcycle_type.id}",
            "data": {
                "motorcycle_type_id": motorcycle_file.motorcycle_type.id,
                "motorcycle_type_name": motorcycle_file.motorcycle_type.get_full_path(),
                "brand_name": motorcycle_file.brand.name,
                "color_name": motorcycle_file.color.name,
                "photos": serializer.data
            }
        }, status=status.HTTP_200_OK)