# Django rest framework
from rest_framework import viewsets, status
from rest_framework.response import Response
# Seralizers
from .serializers import TypePriceModelSerializer
# Models
from ...models.type_price import TypePrice
# Choices
from ...choices.product_type import ProductType
class TypePriceReadOnlyModelViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TypePrice.objects.filter(is_active=True).only("slug", "name", "product_type").order_by("slug")
    serializer_class = TypePriceModelSerializer
    
    def list(self, request, *args, **kwargs):
        product_type = request.query_params.get("product_type")
        # validamos el parámetro si se envía
        if product_type and product_type not in ProductType.values:
            return Response(
                {
                    "success":False,
                    "message": f"Valor inválido para 'product_type': {product_type}. "
                               f"Opciones válidas son: {list(ProductType.values)}",
                    "data": None,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        queryset = self.get_queryset()
        # filtrar si se envió el parámetro
        if product_type in [ProductType.MOTORCYCLE, ProductType.SPAREPART]:
            queryset = queryset.filter(product_type__in=[product_type, ProductType.BOTH])
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)