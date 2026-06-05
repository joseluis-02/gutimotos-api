# Python
from dataclasses import dataclass
from uuid import UUID
 
 
@dataclass
class ListQuotationsRequestDTO:
    user_id: UUID
    page: int = 1
 
 
class ListQuotationsQuery:
 
    def __init__(self, quotation_repository):
        self._repo = quotation_repository
 
    def execute(self, dto: ListQuotationsRequestDTO) -> dict:
        return self._repo.find_by_user(
            user_id=dto.user_id,
            page=dto.page,
        )