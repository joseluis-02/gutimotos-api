# quotations/application/commands/create_quotation_command.py

from datetime import datetime, timedelta
from decimal import Decimal
from typing import Set
from uuid import UUID

from apps.quotations.application.dto.quotation_dto import (
    CreateQuotationRequestDTO,
    QuotationResponseDTO,
    QuotationItemResponseDTO
)
from apps.quotations.domain.repositories.quotation_repository import (
    IProductRepository,
    ITypePriceRepository,
    ICurrencyRepository,
    IQuotationRepository
)
from apps.quotations.domain.services.price_calculator_service import PriceCalculatorService
from apps.quotations.domain.exceptions.quotation_exception import (
    ProductNotFoundException,
    ProductPriceNotFoundException,
    TypePriceNotFoundException,
    CurrencyNotFoundException,
    QuotationItemDuplicatedException
)
from apps.quotations.infrastructure.persistence.models.quotation import Quotation
from apps.quotations.infrastructure.persistence.models.quotation_item import QuotationItem


class CreateQuotationCommand:
    """
    Caso de uso: Crear una nueva cotización
    
    Responsabilidades:
    - Validar datos de entrada
    - Verificar existencia de productos, precios, tipo de precio y moneda
    - Calcular precios con margen de ganancia
    - Crear la cotización y sus items
    - Retornar DTO de respuesta
    """
    
    def __init__(
        self,
        product_repository: IProductRepository,
        type_price_repository: ITypePriceRepository,
        currency_repository: ICurrencyRepository,
        quotation_repository: IQuotationRepository,
        price_calculator: PriceCalculatorService,
        expiration_days: int = 7  # 7 días de expiración
    ):
        self._product_repo = product_repository
        self._type_price_repo = type_price_repository
        self._currency_repo = currency_repository
        self._quotation_repo = quotation_repository
        self._price_calculator = price_calculator
        self._expiration_days = expiration_days
    
    def execute(self, request: CreateQuotationRequestDTO) -> QuotationResponseDTO:
        """
        Ejecuta el comando de creación de cotización
        
        Args:
            request: DTO con los datos de la solicitud
            
        Returns:
            QuotationResponseDTO con la cotización creada
        """
        # 1. Validar que no haya productos duplicados
        self._validate_no_duplicate_products(request)
        
        # 2. Obtener y validar tipo de precio
        type_price = self._type_price_repo.find_by_slug(request.type_price_slug)
        if not type_price:
            raise TypePriceNotFoundException(request.type_price_slug)
        
        # 3. Obtener y validar moneda
        currency = self._currency_repo.find_by_code(request.currency_code)
        if not currency:
            raise CurrencyNotFoundException(request.currency_code)
        
        # 4. Crear la cotización (sin items aún)
        quotation = self._create_quotation_entity(
            user_id=request.user_id,
            profit_margin=type_price.profit_margin,
            currency_code=currency.code,
            whatsapp=request.whatsapp
        )
        
        # 5. Procesar y crear items
        items_data = []
        items_subtotals = []
        
        for item_request in request.items:
            item_data, item_subtotal = self._process_quotation_item(
                quotation=quotation,
                product_code=item_request.product_code,
                quantity=item_request.quantity,
                profit_margin=type_price.profit_margin,
                currency_code=currency.code
            )
            items_data.append(item_data)
            items_subtotals.append(item_subtotal)
        
        # 6. Calcular totales de la cotización
        quotation.subtotal, quotation.total = self._price_calculator.calculate_quotation_totals(
            items_subtotals
        )
        
        # 7. Guardar cotización con items
        saved_quotation = self._quotation_repo.save(quotation)
        
        # 8. Crear items en base de datos
        quotation_items = []
        for item_data in items_data:
            quotation_item = QuotationItem(
                quotation=saved_quotation,
                product_id=item_data['product_id'],
                quantity=item_data['quantity'],
                unit_price=item_data['unit_price'],
                subtotal=item_data['subtotal']
            )
            quotation_item.save()
            quotation_items.append({
                'code': item_data['product_code'],
                'description': item_data['product_description'],
                'quantity': item_data['quantity'],
                'unit_price': item_data['unit_price'],
                'subtotal': item_data['subtotal']
            })
        
        # 9. Construir y retornar DTO de respuesta
        return self._build_response_dto(saved_quotation, quotation_items, currency.symbol)
    
    def _validate_no_duplicate_products(self, request: CreateQuotationRequestDTO) -> None:
        """Valida que no haya códigos de productos duplicados"""
        product_codes: Set[str] = set()
        for item in request.items:
            if item.product_code in product_codes:
                raise QuotationItemDuplicatedException(item.product_code)
            product_codes.add(item.product_code)
    
    def _create_quotation_entity(
        self,
        user_id: UUID,
        profit_margin: Decimal,
        currency_code: str,
        whatsapp: str | None
    ) -> Quotation:
        """Crea la entidad Quotation"""
        now = datetime.now()
        #expired = now + timedelta(days=self._expiration_days)
        expired = now + timedelta(minutes=15)
        
        return Quotation(
            user_id=user_id,
            expired=expired,
            whatsapp=whatsapp,
            profit_margin=profit_margin,
            currency_code=currency_code,
            subtotal=Decimal('0.00'),
            total=Decimal('0.00')
        )
    
    def _process_quotation_item(
        self,
        quotation: Quotation,
        product_code: str,
        quantity: int,
        profit_margin: Decimal,
        currency_code: str
    ) -> tuple[dict, Decimal]:
        """
        Procesa un item de cotización: busca producto, calcula precios
        
        Returns:
            Tupla con (datos del item, subtotal)
        """
        # Buscar producto
        product = self._product_repo.find_by_code(product_code)
        if not product:
            raise ProductNotFoundException(product_code)
        
        # Obtener precio base del producto en la moneda especificada
        base_price = self._product_repo.get_price(product.id, currency_code)
        if base_price is None:
            raise ProductPriceNotFoundException(product_code, currency_code)
        
        # Calcular precio unitario con margen
        unit_price = self._price_calculator.calculate_unit_price(
            base_price=base_price,
            profit_margin=profit_margin
        )
        
        # Calcular subtotal del item
        item_subtotal = self._price_calculator.calculate_item_subtotal(
            unit_price=unit_price,
            quantity=quantity
        )
        
        item_data = {
            'product_id': product.id,  # UUID
            'product_code': product.code,
            'product_description': product.description,  # Product usa 'description' no 'name'
            'quantity': quantity,
            'unit_price': unit_price,
            'subtotal': item_subtotal
        }
        
        return item_data, item_subtotal
    
    def _build_response_dto(
        self,
        quotation: Quotation,
        items: list[dict],
        currency_symbol: str
    ) -> QuotationResponseDTO:
        """Construye el DTO de respuesta"""
        items_dto = [
            QuotationItemResponseDTO(
                product_code=item['code'],
                product_description=item['description'],
                quantity=item['quantity'],
                unit_price=item['unit_price'],
                subtotal=item['subtotal']
            )
            for item in items
        ]
        
        return QuotationResponseDTO(
            id=quotation.id,
            user_id=quotation.user_id,
            created=quotation.created,
            expired=quotation.expired,
            whatsapp=quotation.whatsapp,
            profit_margin=quotation.profit_margin,
            currency_code=quotation.currency_code,
            currency_symbol=currency_symbol,
            subtotal=quotation.subtotal,
            total=quotation.total,
            status=quotation.status,
            items=items_dto
        )