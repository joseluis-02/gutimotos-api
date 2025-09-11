# Django rest framework
from rest_framework import viewsets
# Seralizers
from .serializers import TypePriceModelSerializer
# Models
from ...models.type_price import TypePrice
class TypePriceReadOnlyModelViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TypePrice.objects.filter(is_active=True).only("slug", "name").order_by("slug")
    serializer_class = TypePriceModelSerializer