# Django
from django.db.models import F, Window
from django.db.models.functions import RowNumber
# Django REST Framework
from rest_framework import viewsets
from rest_framework.response import Response
# Models
from ...models.product_photo import ProductPhoto
from apps.core.models.type_price import TypePrice
# Serializers
from .serializers import ProductPhotoSerializer, ProductPhotoListSerializer, ProductPhotoDetailSerializer
# Paginations
from .paginations import ProductPhotoCursorPagination

class ProductPhotoReadOnlyModelViewSet(viewsets.ReadOnlyModelViewSet):
    pagination_class = ProductPhotoCursorPagination

    def get_serializer_class(self):
        if self.action == 'list':
            return ProductPhotoListSerializer
        if self.action == 'retrieve':
            return ProductPhotoDetailSerializer
        return ProductPhotoSerializer

    def get_queryset(self):
        qs = ProductPhoto.objects.select_related(
            'product', 
            'product__brand',
            'product__category'
        ).prefetch_related('product__p_prices')  # Evitar N+1 queries con precios

        if self.action == 'list':
            # Traer solo una foto por producto
            annotated = qs.annotate(
                row_number=Window(
                    expression=RowNumber(),
                    partition_by=[F('product')],
                    order_by=F('created').asc()
                )
            )
            return annotated.filter(row_number=1)

        return qs
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        request = self.request

        currency_code = request.query_params.get("currency", "BOB")  # Valor por defecto BOB
        type_price_slug = request.query_params.get("type_price_slug", "venta-publico")

        type_price = TypePrice.objects.filter(
            slug=type_price_slug, is_active=True
        ).first() if type_price_slug else None

        context.update({
            "currency": currency_code,
            "type_price": type_price
        })
        return context

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        product = instance.product

        # Obtener todas las fotos de esa motocicleta
        queryset = ProductPhoto.objects.filter(product=product).order_by('-created')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)