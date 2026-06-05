# Python
from dataclasses import dataclass
from uuid import UUID
# Domain
from apps.quotations.domain.exceptions.quotation_exception import QuotationNotFoundException
 
 
@dataclass
class GetQuotationItemsRequestDTO:
    quotation_id: UUID
    user_id: UUID
    page: int = 1
 
 
class GetQuotationItemsQuery:
 
    def __init__(self, quotation_repository):
        self._repo = quotation_repository
 
    def execute(self, dto: GetQuotationItemsRequestDTO) -> dict:
        result = self._repo.find_items_by_quotation(
            quotation_id=dto.quotation_id,
            user_id=dto.user_id,
            page=dto.page,
        )
 
        if result is None:
            raise QuotationNotFoundException(dto.quotation_id)
 
        return result