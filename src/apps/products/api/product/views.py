# Django rest framework
from rest_framework.generics import ListAPIView
# Django filters
from django_filters.rest_framework import DjangoFilterBackend
# Models
from ...models.product import Product
from apps.core.models.type_price import TypePrice
# Serializers
from .serializers import ProductListSerializer, ProductTabulatorModelSerializer
# Paginations
from .paginations import ProductListCursorPagination, ProductTabulatorPageNumberPagination
# Queries
from .queries import get_base_product_tabulator_queryset
# Filters
from .filters import ProductTabulatorFilterSet

class ProductListAPIView(ListAPIView):
    serializer_class = ProductListSerializer
    pagination_class = ProductListCursorPagination

    def get_queryset(self):
        return Product.objects.active_with_related()

class ProductTabulatorListAPIView(ListAPIView):
    serializer_class = ProductTabulatorModelSerializer
    pagination_class = ProductTabulatorPageNumberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductTabulatorFilterSet

    def get_queryset(self):
        params = self.request.query_params
        queryset = get_base_product_tabulator_queryset()

        # Ordenación
        sort = params.get("sort", "code")
        dir_ = params.get("dir", "asc")
        if dir_ == "desc":
            sort = f"-{sort}"
        queryset = queryset.order_by(sort)

        return queryset

    def get_serializer_context(self):
        context = super().get_serializer_context()
        type_price_slug = self.request.query_params.get("type_price_slug")
        currency_code = self.request.query_params.get("currency_code")

        context["currency"] = currency_code
        context["type_price"] = TypePrice.objects.filter(slug=type_price_slug, is_active=True).first()
        return context