# Django
from django.db.models import Q
# Django filters
import django_filters
# Models
from ...models.product import Product
# Functions
from .functions import safe_trigram_product_tabulator_search

def apply_product_tabulator_filter(queryset, params):
    brand_id = params.get("brand_id")
    category_id = params.get("category_id")
    search = params.get("search", "").strip()

    if brand_id:
        queryset = queryset.filter(brand_id=brand_id)

    if category_id:
        queryset = queryset.filter(category_id=category_id)

    return safe_trigram_product_tabulator_search(queryset, search)

class ProductTabulatorFilterSet(django_filters.FilterSet):
    brand_id = django_filters.NumberFilter(field_name="brand__id")
    category_id = django_filters.NumberFilter(field_name="category__id")
    search = django_filters.CharFilter(method="filter_search")

    class Meta:
        model = Product
        fields = ["brand_id", "category_id"]

    def filter_search(self, queryset, name, value):
        value = value.strip()
        if not value:
            return queryset

        return queryset.filter(
            Q(code__icontains=value) |
            Q(description__icontains=value) |
            Q(brand__name__icontains=value) |
            Q(category__description_sin__icontains=value)
        )