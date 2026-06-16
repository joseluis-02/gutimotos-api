# Python
from typing import Tuple
import logging
# Django
from django.utils import timezone
from django.contrib.sessions.models import Session
# Simple JWT
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken
# Logger
logger = logging.getLogger(__name__)

def clean_expired_outstanding_tokens() -> Tuple[int, str]:
    """
    Responsabilidad Única: Eliminar tokens OutstandingToken expirados.
    """
    now_local = timezone.localtime(timezone.now())
    
    # 1. Obtener tokens expirados
    expired_tokens_qs = OutstandingToken.objects.filter(expires_at__lt=now_local)
    expired_count = expired_tokens_qs.count()

    # 2. Eliminar (si hay)
    if expired_count > 0:
        expired_tokens_qs.delete()
    
    summary = f"Eliminados {expired_count} tokens expirados."
    return expired_count, summary

def clean_revoked_outstanding_tokens() -> Tuple[int, str]:
    """
    Responsabilidad Única: Eliminar tokens OutstandingToken que han sido revocados.
    """
    # 1. Obtener tokens revocados (los que tienen una entrada BlacklistedToken)
    # Utilizamos select_related para optimizar la consulta si fuera necesario, 
    # aunque aquí el filtro directo es suficiente.
    revoked_tokens_qs = OutstandingToken.objects.filter(blacklistedtoken__isnull=False)
    revoked_count = revoked_tokens_qs.count()

    # 2. Eliminar (si hay)
    if revoked_count > 0:
        revoked_tokens_qs.delete()
    
    summary = f"Eliminados {revoked_count} tokens revocados."
    return revoked_count, summary

def clean_blacklisted_orphans() -> Tuple[int, str]:
    """
    Responsabilidad Única: Eliminar registros BlacklistedToken sin OutstandingToken asociado (huérfanos).
    """
    # 1. Obtener tokens huérfanos
    blacklisted_orphans_qs = BlacklistedToken.objects.filter(token__isnull=True)
    blacklist_count = blacklisted_orphans_qs.count()

    # 2. Eliminar (si hay)
    if blacklist_count > 0:
        blacklisted_orphans_qs.delete()

    summary = f"Eliminados {blacklist_count} blacklisted huérfanos."
    return blacklist_count, summary

def run_all_token_cleanup_tasks():
    total_cleaned = 0
    full_report = "--- Reporte de Limpieza de Tokens ---\n"
    # Llamamos a la función directamente ya que está en el mismo archivo.
    expired_count, summary_exp = clean_expired_outstanding_tokens()
    total_cleaned += expired_count
    full_report += f"1. {summary_exp}\n"
    
    # 2. Ejecutar Tarea: Limpieza de Revocados
    revoked_count, summary_rev = clean_revoked_outstanding_tokens()
    total_cleaned += revoked_count
    full_report += f"2. {summary_rev}\n"

    # 3. Ejecutar Tarea: Limpieza de Huérfanos
    blacklist_count, summary_orph = clean_blacklisted_orphans()
    total_cleaned += blacklist_count
    full_report += f"3. {summary_orph}\n"

    # --- Resumen Final ---
    
    final_message = f"✅ Limpieza de Tokens Finalizada. Total de registros eliminados: {total_cleaned}"
    full_report += final_message
    
    # Loguear el resultado final para monitoreo
    logger.info(full_report)
    
    return final_message

def limpiar_sesiones_expiradas():
    """
    Limpia sesiones expiradas de Django
    """
    resultado = Session.objects.filter(
        expire_date__lt=timezone.now()
    ).delete()
    
    sesiones_eliminadas = resultado[0]
    
    logger.info(f"[CLEANUP] Sesiones eliminadas: {sesiones_eliminadas}")
    
    return {'sesiones_eliminadas': sesiones_eliminadas}