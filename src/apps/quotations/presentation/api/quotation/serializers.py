# Django Rest
from rest_framework import serializers
# Domain - choices
from apps.quotations.domain.choices.quotation_status import QuotationStatus

class QuotationItemRequestSerializer(serializers.Serializer):
    """Serializer para un item de cotización en el request"""
    product_code = serializers.CharField(
        max_length=50,
        required=True,
        help_text="Código del producto"
    )
    quantity = serializers.IntegerField(
        min_value=1,
        required=True,
        help_text="Cantidad del producto"
    )


class CreateQuotationRequestSerializer(serializers.Serializer):
    """Serializer para la creación de una cotización"""
    items = serializers.ListField(
        child=QuotationItemRequestSerializer(),
        min_length=1,
        required=True,
        help_text="Lista de items de la cotización"
    )
    type_price_slug = serializers.SlugField(
        required=True,
        help_text="Slug del tipo de precio a aplicar"
    )
    currency_code = serializers.CharField(
        max_length=3,
        required=True,
        help_text="Código de la moneda (USD, BOB, etc.)"
    )
    whatsapp = serializers.CharField(
        max_length=20,
        required=False,
        allow_null=True,
        allow_blank=True,
        help_text="Número de WhatsApp (opcional)"
    )
    
    def validate_items(self, value):
        """Valida que no haya productos duplicados"""
        product_codes = [item['product_code'] for item in value]
        if len(product_codes) != len(set(product_codes)):
            raise serializers.ValidationError(
                "No puede haber productos duplicados en la cotización"
            )
        return value


class QuotationItemResponseSerializer(serializers.Serializer):
    """Serializer para un item de cotización en la respuesta"""
    product_code = serializers.CharField()
    product_description = serializers.CharField()
    quantity = serializers.IntegerField()
    unit_price = serializers.DecimalField(max_digits=12, decimal_places=2)
    subtotal = serializers.DecimalField(max_digits=12, decimal_places=2)


class QuotationResponseSerializer(serializers.Serializer):
    """Serializer para la respuesta de una cotización"""
    id = serializers.UUIDField()
    user_id = serializers.UUIDField()
    created = serializers.DateTimeField()
    expired = serializers.DateTimeField()
    whatsapp = serializers.CharField(allow_null=True)
    profit_margin = serializers.DecimalField(max_digits=5, decimal_places=2)
    currency_code = serializers.CharField()
    currency_symbol = serializers.CharField()
    subtotal = serializers.DecimalField(max_digits=12, decimal_places=2)
    total = serializers.DecimalField(max_digits=12, decimal_places=2)
    status = serializers.CharField()
    items = QuotationItemResponseSerializer(many=True)


class UpdateQuotationStatusRequestSerializer(serializers.Serializer):
    """Serializer para actualizar estado de cotización"""
    status = serializers.ChoiceField(
        choices=[
            QuotationStatus.CONFIRMED,
            QuotationStatus.CANCELLED
        ],
        required=True,
        help_text="Nuevo estado: CONFIRMED o CANCELLED"
    )


class UpdateQuotationStatusResponseSerializer(serializers.Serializer):
    """Serializer de respuesta al actualizar estado"""
    quotation_id = serializers.UUIDField()
    status = serializers.CharField()
    message = serializers.CharField()

# Actualizar los items de la cotización
class UpdateQuotationItemRequestSerializer(serializers.Serializer):
    """Serializer para item a actualizar"""
    product_code = serializers.CharField(max_length=50, required=True)
    quantity = serializers.IntegerField(min_value=1, required=True)


class UpdateQuotationItemsRequestSerializer(serializers.Serializer):
    """Serializer para actualizar items"""
    items = serializers.ListField(
        child=UpdateQuotationItemRequestSerializer(),
        min_length=1,
        required=True
    )
    
    def validate_items(self, value):
        """Valida que no haya productos duplicados"""
        product_codes = [item['product_code'] for item in value]
        if len(product_codes) != len(set(product_codes)):
            raise serializers.ValidationError("Productos duplicados")
        return value