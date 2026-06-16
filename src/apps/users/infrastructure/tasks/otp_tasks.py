# Users - Domain
from apps.users.domain.services.otp_cleanup_service import OTPCleanupService

def cleanup_expired_otps_task():
    """Tarea: Limpiar OTPs expirados"""
    return OTPCleanupService.delete_expired_otps(days=1)