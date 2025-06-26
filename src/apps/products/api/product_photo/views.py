# Django
from django.db.models import F, Window
from django.db.models.functions import RowNumber
# Django REST Framework
from rest_framework import viewsets
from rest_framework.response import Response
# Models
from ...models.product_photo import ProductPhoto
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
        qs = ProductPhoto.objects.all().select_related(
            'product',
        )
        if self.action == 'list':
            # Aquí aplicá el filtro para una foto por motorcycle_file, como te mostré antes
            annotated = qs.annotate(
                row_number=Window(
                    expression=RowNumber(),
                    partition_by=[F('product')],
                    order_by=F('created').asc()
                )
            )
            return annotated.filter(row_number=1)
        return qs

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        product = instance.product

        # Obtener todas las fotos de esa motocicleta
        queryset = ProductPhoto.objects.filter(product=product).order_by('-created')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)