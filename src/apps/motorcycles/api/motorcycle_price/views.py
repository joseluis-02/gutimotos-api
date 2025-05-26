# Python
from decimal import Decimal
# Django
from django.shortcuts import get_object_or_404
# Django rest framework
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# Models
from ...models import MotorcyclePrice, MotorcycleType
from apps.core.models import Brand
from apps.prices.models import TypePrice
# Serializers
from .serializers import CalculatedPriceByCurrencySerializer

class MotorcycleMultiCurrencyPriceAPIView(APIView):
    def get(self, request):
        slug_type_price = request.query_params.get("slug_type_price")
        brand_id = request.query_params.get("brand_id")
        motorcycle_type_id = request.query_params.get("motorcycle_type_id")

        # Validación de parámetros requeridos
        if not all([slug_type_price, brand_id, motorcycle_type_id]):
            return Response(
                {"detail": "Faltan parámetros requeridos: slug_type_price, brand_id, motorcycle_type_id"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Obtener objetos
        type_price = get_object_or_404(TypePrice, slug=slug_type_price)
        brand = get_object_or_404(Brand, id=brand_id)
        motorcycle_type = get_object_or_404(MotorcycleType, id=motorcycle_type_id)

        # Filtrar precios base existentes para esa combinación
        prices = MotorcyclePrice.objects.filter(
            brand=brand,
            motorcycle_type=motorcycle_type
        ).select_related('currency')

        if not prices.exists():
            return Response(
                {"detail": "No se encontraron precios base para la marca, tipo de motocicleta y tipo de precio."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Construir lista de precios calculados
        result = []
        for price in prices:
            margin = type_price.profit_margin
            final_price = price.base + (price.base * margin / Decimal(100))
            result.append({
                "currency": price.currency.name,
                "final_price": final_price.quantize(Decimal("0.01"))
            })

        serializer = CalculatedPriceByCurrencySerializer(result, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
