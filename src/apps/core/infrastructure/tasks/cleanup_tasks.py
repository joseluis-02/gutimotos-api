# Application
from apps.core.application.services.infrastructure_cleanup_service import InfrastructureCleanupService

def cleanup_django_sessions_task():
    """Tarea programada: Limpiar sesiones expiradas de Django"""
    return InfrastructureCleanupService.cleanup_expired_sessions()