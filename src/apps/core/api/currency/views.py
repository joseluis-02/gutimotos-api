# Django rest framework
from rest_framework import viewsets
# Seralizers
from .serializers import CurrencyModelSerializer
# Models
from ...models.currency import Currency
class CurrencyReadOnlyModelViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Currency.objects.filter(is_active=True).only("code", "name", "symbol").order_by("code")
    serializer_class = CurrencyModelSerializer