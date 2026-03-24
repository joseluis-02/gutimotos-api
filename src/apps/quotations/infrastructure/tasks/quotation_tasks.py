# AGREGAR esta tarea
from apps.quotations.application.services.quotation_notification_service import QuotationNotificationService
from apps.quotations.application.services.quotation_expiration_service import QuotationExpirationService
from apps.quotations.application.services.quotation_cleanup_service import QuotationCleanupService

def notify_expiring_quotations_task():
    """Tarea: Notificar cotizaciones próximas a expirar"""
    return QuotationNotificationService.notify_expiring_quotations(hours_before=24)


def expire_quotations_task():
    """Tarea: Marcar cotizaciones vencidas como EXPIRED"""
    return QuotationExpirationService.expire_quotations()


def cleanup_cancelled_quotations_task():
    """Tarea: Eliminar todas las cotizaciones canceladas"""
    return QuotationCleanupService.delete_cancelled_quotations()


def cleanup_old_expired_quotations_task():
    """Tarea: Eliminar cotizaciones expiradas hace más de 7 días"""
    return QuotationCleanupService.delete_old_expired_quotations(days=7)