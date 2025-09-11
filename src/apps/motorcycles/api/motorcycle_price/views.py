# Django REST Framework
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
# Simple JWT
from rest_framework_simplejwt.authentication import JWTAuthentication
# Models
from ...models import MotorcyclePrice, MotorcycleType
from apps.core.models.type_price import TypePrice


class MotorcyclePricesByMotorcycleTypeAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, motorcycle_type_id, type_price_slug):
        # 1. Buscar el tipo de precio
        try:
            type_price = TypePrice.objects.get(slug=type_price_slug)
        except TypePrice.DoesNotExist:
            return Response(
                {
                    "success": False,
                    "message": f"No existe TypePrice activo con slug='{type_price_slug}'",
                    "data": None,
                },
                status=status.HTTP_404_NOT_FOUND,
            )
        # 2. Validaciones y búsqueda de precios base
        try:
            motorcycle_type = MotorcycleType.objects.get(id=motorcycle_type_id)
        except MotorcycleType.DoesNotExist:
            return Response(
                {
                    "success": False,
                    "message": f"No existe una motorcycle_type con id={motorcycle_type_id}",
                    "data": None,
                },
                status=status.HTTP_404_NOT_FOUND,
            )
        # Buscar todos los precios base para el tipo de motocicleta
        prices = MotorcyclePrice.objects.filter(
            motorcycle_type=motorcycle_type
        ).select_related("currency")
        # Si no hay precios, devolvemos lista vacía pero success=True
        if not prices.exists():
            return Response(
                {
                    "success": True,
                    "message": "No existen precios registrados para este tipo de motocicleta",
                    "data": {
                        "type_price_name": type_price.name,
                        "prices": [],
                    },
                },
                status=status.HTTP_200_OK,
            )
        # 3. Construir lista de precios finales
        results = []
        for p in prices:
            final_price = type_price.calculate_price_motorcycle(p.base)
            results.append({
                "currency_name": p.currency.name,
                "currency_code": p.currency.code,
                "final_price": int(final_price),
            })
        return Response(
            {
                "success": True,
                "message": "Lista de precios calculada exitosamente",
                "data": {
                    "type_price_name": type_price.name,
                    "prices": results,
                },
            },
            status=status.HTTP_200_OK,
        )
