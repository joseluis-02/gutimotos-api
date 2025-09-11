# Django rest framework
from rest_framework import viewsets
# Seralizers
from .serializers import BrandSelectSerializer
# Paginations
from .paginations import BrandPageNumberPagination
# Models
from ...models.brand import Brand
class BrandSelectReadOnlyModelViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Brand.objects.filter(is_active=True).only("id", "name").order_by("name")
    serializer_class = BrandSelectSerializer
    pagination_class = BrandPageNumberPagination