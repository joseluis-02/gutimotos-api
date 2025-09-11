# Django
from django.db.models import Q
# Django REST Framework
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
# Simple JWT
from rest_framework_simplejwt.authentication import JWTAuthentication
# Django Filters
from django_filters.rest_framework import DjangoFilterBackend
# Models
from ...models.product_photo import ProductPhoto
from apps.core.models.type_price import TypePrice
# Serializers
from .serializers import ProductPhotoListSerializer, ProductPhotoDetailSerializer
# Paginations
from .paginations import ProductPhotoCursorPagination
# Filters
from .filters import ProductPhotoFilterSet

class ProductPhotoReadOnlyModelViewSet(viewsets.ReadOnlyModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductPhotoFilterSet
    pagination_class = ProductPhotoCursorPagination

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ProductPhotoDetailSerializer
        return ProductPhotoListSerializer

    def get_queryset(self):
        qs = ProductPhoto.objects.select_related(
            'product', 
            'product__brand',
            'product__category'
        ).prefetch_related('product__p_prices')

        # 1. Filtro por marca, categoría u otros filtros de FilterSet
        qs = self.filter_queryset(qs)

        # 2. Búsqueda profunda con Q
        search = self.request.query_params.get('search')
        if search:
            qs = qs.filter(
                Q(product__description__icontains=search) |
                Q(product__code__icontains=search) |
                Q(product__brand__name__icontains=search)
            )

        # 3. Solo una foto por producto
        if self.action == 'list':
            from django.db.models import F, Window
            from django.db.models.functions import RowNumber
            annotated = qs.annotate(
                row_number=Window(
                    expression=RowNumber(),
                    partition_by=[F('product')],
                    order_by=F('created').asc()
                )
            )
            qs = annotated.filter(row_number=1)

        return qs
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        request = self.request

        # Parámetros con valores por defecto
        currency_code = request.query_params.get("currency_code", "BOB")
        type_price_slug = request.query_params.get("type_price_slug", "venta-publico")

        type_price = None
        if type_price_slug:
            try:
                type_price = TypePrice.objects.get(slug=type_price_slug, is_active=True)
            except TypePrice.DoesNotExist:
                type_price = None  # Si no existe, mantenemos None

        context.update({
            "currency_code": currency_code,
            "type_price": type_price,
        })
        return context

    def retrieve(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
    
        # Validar que sea un entero
        try:
            pk = int(pk)
        except (TypeError, ValueError):
            return Response(
                {
                    "success": False,
                    "message": f"El ID '{kwargs.get('pk')}' no es válido.",
                    "data": None
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # Buscar instancia
        try:
            instance = self.get_queryset().get(pk=pk)
        except self.get_queryset().model.DoesNotExist:
            return Response(
                {
                    "success": False,
                    "message": f"No se encontró un registro con ID={pk}",
                    "data": None
                },
                status=status.HTTP_404_NOT_FOUND
            )

        product = instance.product

        # Obtener todas las fotos
        queryset = ProductPhoto.objects.filter(product=product).order_by('-created')
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "success": True,
            "message": f"Se ha obtenido las fotos de un producto con ID:{pk}",
            "data": {
                "product_code": product.code,
                "photos": serializer.data
            }
        }, status=status.HTTP_200_OK)