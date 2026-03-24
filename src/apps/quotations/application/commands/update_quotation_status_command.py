# Python
from uuid import UUID
import logging
# application
from apps.quotations.application.dto.quotation_dto import (
    UpdateQuotationStatusRequestDTO,
    UpdateQuotationStatusResponseDTO
)
from apps.quotations.application.services.quotation_email_service import QuotationEmailService
# domain
from apps.quotations.domain.choices.quotation_status import QuotationStatus
from apps.quotations.domain.repositories.quotation_repository import IQuotationRepository
from apps.quotations.domain.exceptions.quotation_exception import (
    InvalidStatusTransitionException,
    QuotationNotFoundException,
    UnauthorizedStatusChangeException
)


class UpdateQuotationStatusCommand:
    """
    Caso de uso: Actualizar estado de cotización (Usuario)
    
    Responsabilidades:
    - Validar que la cotización existe
    - Validar permisos del usuario
    - Validar que está en estado REVIEWED
    - Validar transición de estado
    - Actualizar el estado
    """
    
    def __init__(self, quotation_repository: IQuotationRepository):
        self._quotation_repo = quotation_repository
    
    def execute(self, request: UpdateQuotationStatusRequestDTO) -> UpdateQuotationStatusResponseDTO:
        # 1. Buscar cotización
        quotation = self._quotation_repo.find_by_id(request.quotation_id)
        if not quotation:
            raise QuotationNotFoundException(str(request.quotation_id))
        
        # 2. Validar permisos
        self._validate_ownership(quotation, request.user_id)
        
        # 3. Validar estado actual
        self._validate_current_status(quotation)
        
        # 4. Validar transición
        self._validate_transition(quotation.status, request.new_status)
        
        # 5. Actualizar estado
        quotation.set_status(request.new_status)
        self._quotation_repo.save(quotation)
        
        # 6. Si es confirmación, enviar email con PDF
        if request.new_status == QuotationStatus.CONFIRMED:
            self._send_confirmation_email(quotation)
        
        # 7. Retornar respuesta
        return UpdateQuotationStatusResponseDTO(
            quotation_id=quotation.id,
            status=quotation.status,
            message=f"Estado actualizado a {quotation.get_status_display()}"
        )

    def _send_confirmation_email(self, quotation) -> None:
        """Envía email de confirmación con PDF"""
        items = []
        for item in quotation.items.all():
            items.append({
                'product_code': item.product.code,
                'product_description': item.product.description,
                'quantity': item.quantity,
                'unit_price': item.unit_price,
                'subtotal': item.subtotal
            })
        
        # Enviar email (no bloqueante, error no detiene el proceso)
        try:
            QuotationEmailService.send_quotation_confirmation_email(quotation, items)
        except Exception as e:
            logger = logging.getLogger(__name__)
            logger.error(f"Error enviando email de confirmación: {str(e)}")
            # No lanzar excepción, el estado ya se actualizó
    
    def _validate_ownership(self, quotation, user_id: UUID) -> None:
        """Valida que el usuario sea el dueño de la cotización"""
        if quotation.user_id != user_id:
            raise UnauthorizedStatusChangeException(
                "Solo el dueño puede modificar esta cotización"
            )
    
    def _validate_current_status(self, quotation) -> None:
        """Valida que la cotización esté en estado REVIEWED"""
        if quotation.status != QuotationStatus.REVIEWED:
            raise UnauthorizedStatusChangeException(
                "Solo se puede confirmar/cancelar cotizaciones revisadas"
            )
    
    def _validate_transition(self, current_status: str, new_status: str) -> None:
        """Valida que la transición sea válida"""
        valid_transitions = QuotationStatus.valid_transitions(current_status)
        if new_status not in valid_transitions:
            raise InvalidStatusTransitionException(current_status, new_status)