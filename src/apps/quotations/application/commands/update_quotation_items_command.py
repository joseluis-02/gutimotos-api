# quotations/application/commands/update_quotation_items_command.py

from uuid import UUID
from decimal import Decimal
from typing import List
from apps.quotations.application.dto.quotation_dto import (
    UpdateQuotationItemsRequestDTO,
    UpdateQuotationItemsResponseDTO,
    QuotationItemResponseDTO
)
from apps.quotations.domain.repositories.quotation_repository import (
    IQuotationRepository,
    IProductRepository
)
from apps.quotations.domain.services.price_calculator_service import PriceCalculatorService
from apps.quotations.domain.choices.quotation_status import QuotationStatus
from apps.quotations.domain.exceptions.quotation_exception import (
    QuotationNotFoundException,
    UnauthorizedStatusChangeException,
    InvalidQuotationStateException,
    ProductNotFoundException,
    ProductPriceNotFoundException,
    QuotationItemDuplicatedException
)


class UpdateQuotationItemsCommand:
    """
    Caso de uso: Actualizar items de cotización
    
    Responsabilidades:
    - Validar que cotización existe y es del usuario
    - Validar que está en estado CREATED
    - Validar productos y precios
    - Eliminar items actuales
    - Crear nuevos items
    - Recalcular totales
    """
    
    def __init__(
        self,
        quotation_repository: IQuotationRepository,
        product_repository: IProductRepository,
        price_calculator: PriceCalculatorService
    ):
        self._quotation_repo = quotation_repository
        self._product_repo = product_repository
        self._price_calculator = price_calculator
    
    def execute(self, request: UpdateQuotationItemsRequestDTO) -> UpdateQuotationItemsResponseDTO:
        """Ejecuta actualización de items"""
        
        # 1. Buscar cotización
        quotation = self._quotation_repo.find_by_id(request.quotation_id)
        if not quotation:
            raise QuotationNotFoundException(str(request.quotation_id))
        
        # 2. Validar ownership
        if quotation.user_id != request.user_id:
            raise UnauthorizedStatusChangeException(
                "Solo el dueño puede modificar esta cotización"
            )
        
        # 3. Validar estado CREATED
        if quotation.status != QuotationStatus.CREATED:
            raise InvalidQuotationStateException(
                quotation.status,
                QuotationStatus.CREATED
            )
        
        # 4. Validar no duplicados
        self._validate_no_duplicates(request.items)
        
        # 5. Eliminar items actuales
        self._quotation_repo.delete_items(quotation)
        
        # 6. Procesar nuevos items
        items_data = []
        items_subtotals = []
        
        for item_dto in request.items:
            item_data, subtotal = self._process_item(
                quotation=quotation,
                product_code=item_dto.product_code,
                quantity=item_dto.quantity
            )
            items_data.append(item_data)
            items_subtotals.append(subtotal)
        
        # 7. Recalcular totales
        quotation.subtotal, quotation.total = self._price_calculator.calculate_quotation_totals(
            items_subtotals
        )
        self._quotation_repo.save(quotation)
        
        # 8. Crear items en BD
        from apps.quotations.infrastructure.persistence.models.quotation_item import QuotationItem
        
        response_items = []
        for item_data in items_data:
            quotation_item = QuotationItem(
                quotation=quotation,
                product_id=item_data['product_id'],
                quantity=item_data['quantity'],
                unit_price=item_data['unit_price'],
                subtotal=item_data['subtotal']
            )
            quotation_item.save()
            
            response_items.append(
                QuotationItemResponseDTO(
                    product_code=item_data['product_code'],
                    product_description=item_data['product_description'],
                    quantity=item_data['quantity'],
                    unit_price=item_data['unit_price'],
                    subtotal=item_data['subtotal']
                )
            )
        
        # 9. Retornar respuesta
        return UpdateQuotationItemsResponseDTO(
            quotation_id=quotation.id,
            subtotal=quotation.subtotal,
            total=quotation.total,
            items=response_items
        )
    
    def _validate_no_duplicates(self, items: List) -> None:
        """Valida que no haya productos duplicados"""
        product_codes = [item.product_code for item in items]
        if len(product_codes) != len(set(product_codes)):
            duplicates = [code for code in product_codes if product_codes.count(code) > 1]
            raise QuotationItemDuplicatedException(duplicates[0])
    
    def _process_item(self, quotation, product_code: str, quantity: int) -> tuple:
        """Procesa un item: busca producto y calcula precios"""
        
        # Buscar producto
        product = self._product_repo.find_by_code(product_code)
        if not product:
            raise ProductNotFoundException(product_code)
        
        # Obtener precio base
        base_price = self._product_repo.get_price(product.id, quotation.currency_code)
        if base_price is None:
            raise ProductPriceNotFoundException(product_code, quotation.currency_code)
        
        # Calcular precio con margen
        unit_price = self._price_calculator.calculate_unit_price(
            base_price=base_price,
            profit_margin=quotation.profit_margin
        )
        
        # Calcular subtotal
        item_subtotal = self._price_calculator.calculate_item_subtotal(
            unit_price=unit_price,
            quantity=quantity
        )
        
        return {
            'product_id': product.id,
            'product_code': product.code,
            'product_description': product.description,
            'quantity': quantity,
            'unit_price': unit_price,
            'subtotal': item_subtotal
        }, item_subtotal