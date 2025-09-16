# Django rest framework
from rest_framework import viewsets
# Seralizers
from .serializers import ColorModelSerializer
# Models
from ...models.color import Color
# Paginations
from .paginations import ColorPageNumberPagination

class ColorReadOnlyModelViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Color.objects.filter(is_active=True).only("id", "name", "code_hex").order_by("name")
    serializer_class = ColorModelSerializer
    pagination_class = ColorPageNumberPagination