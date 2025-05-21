# Python
import logging
# Django
from django.core.management.base import BaseCommand
from django.utils import timezone
# SimpleJWT
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Elimina tokens expirados, revocados y blacklisted huérfanos'

    def handle(self, *args, **kwargs):
        # Hora actual de Bolivia
        now_local = timezone.localtime(timezone.now())
        self.stdout.write(f"Hora actual (Bolivia): {now_local}")

        # 1. Eliminar OutstandingTokens expirados
        expired_tokens = OutstandingToken.objects.filter(expires_at__lt=now_local)
        expired_count = expired_tokens.count()
        expired_tokens.delete()

        # 2. Eliminar OutstandingTokens revocados (tokens en BlacklistedToken)
        revoked_tokens = OutstandingToken.objects.filter(blacklistedtoken__isnull=False)
        revoked_count = revoked_tokens.count()
        revoked_tokens.delete()

        # 3. Eliminar BlacklistedTokens huérfanos (sin OutstandingToken relacionado)
        blacklisted_orphans = BlacklistedToken.objects.filter(token__isnull=True)
        blacklist_count = blacklisted_orphans.count()
        blacklisted_orphans.delete()

        # Log y mensaje final
        summary = (
            f"✔ Eliminados {expired_count} tokens expirados\n"
            f"✔ Eliminados {revoked_count} tokens revocados\n"
            f"✔ Eliminados {blacklist_count} blacklisted huérfanos"
        )

        self.stdout.write(self.style.SUCCESS(summary))
        logger.info(f"[TOKENS] Limpieza completada → {summary}")
