# filters.py
import django_filters
from ....models.product_photo import ProductPhoto

class ProductPhotoFilter(django_filters.FilterSet):
    category = django_filters.NumberFilter(field_name='product__category_id')
    brand = django_filters.NumberFilter(field_name='product__brand_id')
    country = django_filters.NumberFilter(field_name='product__country_id')
    measure = django_filters.NumberFilter(field_name='product__measure_id')
    code = django_filters.CharFilter(field_name='product__code', lookup_expr='iexact')

    class Meta:
        model = ProductPhoto
        fields = ['category', 'brand', 'country', 'measure', 'code']
