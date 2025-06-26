# apps/products/views.py
from rest_framework.generics import ListAPIView
from ...models.product import Product
from .serializers import ProductListSerializer
from .paginations import ProductListCursorPagination

class ProductListAPIView(ListAPIView):
    serializer_class = ProductListSerializer
    pagination_class = ProductListCursorPagination

    def get_queryset(self):
        return Product.objects.active_with_related()
