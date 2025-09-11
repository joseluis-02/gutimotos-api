# Django Filters
import django_filters
# Models
from ...models.product_photo import ProductPhoto

class ProductPhotoFilterSet(django_filters.FilterSet):
    # Filtrado exacto por id de la marca
    brand_id = django_filters.NumberFilter(field_name='product__brand_id', lookup_expr='exact')

    # Puedes mantener otros filtros
    category_id = django_filters.NumberFilter(field_name='product__category_id', lookup_expr='exact')

    class Meta:
        model = ProductPhoto
        fields = ['brand_id', 'category_id']