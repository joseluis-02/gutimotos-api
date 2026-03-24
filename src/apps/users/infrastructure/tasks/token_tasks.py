# Application
from apps.users.application.services.token_management_service import TokenManagementService

def cleanup_expired_tokens_task():
    """Tarea programada: Limpiar todos los tokens JWT expirados"""
    return TokenManagementService.cleanup_all_expired_tokens()