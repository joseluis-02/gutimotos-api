# Crear Cotizacion
class QuotationDomainException(Exception):
    """Excepción base para el dominio de cotizaciones"""
    pass


class ProductNotFoundException(QuotationDomainException):
    """El producto no fue encontrado"""
    def __init__(self, product_code: str):
        self.product_code = product_code
        super().__init__(f"Producto con código '{product_code}' no encontrado")


class ProductPriceNotFoundException(QuotationDomainException):
    """El precio del producto en la moneda especificada no fue encontrado"""
    def __init__(self, product_code: str, currency_code: str):
        self.product_code = product_code
        self.currency_code = currency_code
        super().__init__(
            f"Precio no encontrado para el producto '{product_code}' "
            f"en la moneda '{currency_code}'"
        )


class TypePriceNotFoundException(QuotationDomainException):
    """El tipo de precio no fue encontrado"""
    def __init__(self, slug: str):
        self.slug = slug
        super().__init__(f"Tipo de precio con slug '{slug}' no encontrado")


class CurrencyNotFoundException(QuotationDomainException):
    """La moneda no fue encontrada o no está activa"""
    def __init__(self, code: str):
        self.code = code
        super().__init__(f"Moneda con código '{code}' no encontrada o no activa")


class QuotationItemDuplicatedException(QuotationDomainException):
    """Item duplicado en la cotización"""
    def __init__(self, product_code: str):
        self.product_code = product_code
        super().__init__(f"El producto '{product_code}' ya existe en la cotización")


# Para actualizar estado de la Cotizacion       
class InvalidStatusTransitionException(QuotationDomainException):
    """Transición de estado inválida"""
    def __init__(self, current: str, new: str):
        super().__init__(
            f"No se puede cambiar de '{current}' a '{new}'"
        )

class QuotationNotFoundException(QuotationDomainException):
    """Cotización no encontrada"""
    def __init__(self, quotation_id: str):
        super().__init__(f"Cotización '{quotation_id}' no encontrada")


class UnauthorizedStatusChangeException(QuotationDomainException):
    """Usuario no autorizado para cambiar estado"""
    def __init__(self, message: str):
        super().__init__(message)

# Validación para actualizar la lista de itemes de la cotización
class InvalidQuotationStateException(QuotationDomainException):
    """Estado de cotización no permite la operación"""
    def __init__(self, current_state: str, required_state: str):
        super().__init__(
            f"La cotización debe estar en estado '{required_state}', "
            f"estado actual: '{current_state}'"
        )