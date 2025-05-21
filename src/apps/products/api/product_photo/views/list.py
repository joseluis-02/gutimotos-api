# Python
from decimal import Decimal
from rest_framework.generics import ListAPIView
from django.db.models import OuterRef, Exists, Prefetch
from django.contrib.postgres.search import TrigramSimilarity
from django.db.models import Q
from rest_framework.exceptions import ValidationError

from ....models import ProductPhoto, ProductPrice
from apps.prices.models import TypePrice
from ..serializers import ProductPhotoListSerializer
from ..filters import ProductPhotoFilter
from ..paginations import ProductPhotoListCursorPagination

from django_filters.rest_framework import DjangoFilterBackend


class ProductPhotoListAPIView(ListAPIView):
    serializer_class = ProductPhotoListSerializer
    pagination_class = ProductPhotoListCursorPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductPhotoFilter

    def get_queryset(self):
        search = self.request.query_params.get('search', '').strip()
        currency_code = self.request.query_params.get('currency_code')

        if currency_code:
            prices_with_currency = ProductPrice.objects.filter(
                product=OuterRef('product_id'),
                currency__code=currency_code
            )
            qs = ProductPhoto.objects.annotate(
                has_currency_price=Exists(prices_with_currency)
            ).filter(has_currency_price=True)

            price_qs = ProductPrice.objects.filter(
                currency__code=currency_code
            ).select_related('currency')

            qs = qs.prefetch_related(
                Prefetch('product__p_prices', queryset=price_qs, to_attr='filtered_prices')
            )
        else:
            qs = ProductPhoto.objects.all().prefetch_related(
                'product__p_prices', 'product__p_prices__currency'
            )

        qs = qs.select_related('product')

        # Búsqueda con Trigram
        if search:
            qs = qs.annotate(
                similarity=TrigramSimilarity('product__description', search)
            ).filter(similarity__gt=0.2).order_by('-similarity')

        return qs

    def get_serializer_context(self):
        context = super().get_serializer_context()
        type_price_slug = self.request.query_params.get('type_price_slug')
        if type_price_slug:
            try:
                type_price = TypePrice.objects.get(slug=type_price_slug.strip(), is_active=True)
                context['profit_margin'] = type_price.profit_margin or Decimal('0.00')
            except TypePrice.DoesNotExist:
                raise ValidationError({'message': 'El parámetro (type_price_slug) no válido o inactivo.'})
        else:
            raise ValidationError({'message': 'El parámetro (type_price_slug) es requerido para listar.'})
        return context
