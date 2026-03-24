from django.db import models

class QuotationStatus(models.TextChoices):
    CREATED   = "CREATED", "Creado"       # Cotización recién creada
    REVIEWED  = "REVIEWED", "Revisado"    # Revisada por admin o vendedor
    CONFIRMED = "CONFIRMED", "Confirmado" # Confirmada por el cliente
    CANCELLED = "CANCELLED", "Cancelado"  # Cotización cancelada
    EXPIRED   = "EXPIRED", "Expirado"     # Cotización expirada automáticamente

    @classmethod
    def valid_transitions(cls, current_status):
        """
        Devuelve los estados a los que se puede mover desde el estado actual.
        """
        transitions = {
            cls.CREATED: [cls.REVIEWED, cls.CANCELLED],
            cls.REVIEWED: [cls.CONFIRMED, cls.CANCELLED],
            cls.CONFIRMED: [],
            cls.CANCELLED: [],
            cls.EXPIRED: [],
        }
        return transitions.get(current_status, [])
