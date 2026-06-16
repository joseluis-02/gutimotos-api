# Importar modelos desde su ubicación real
from apps.quotations.infrastructure.persistence.models import (
    Quotation,
    QuotationItem
)

# Exponer para Django
__all__ = [
    Quotation,
    QuotationItem
]