# Django
from django.core.management.base import BaseCommand
# Application
from apps.core.application.services.infrastructure_cleanup_service import InfrastructureCleanupService

class Command(BaseCommand):
    help = 'Limpia sesiones expiradas de Django'

    def handle(self, *args, **options):
        self.stdout.write('Limpiando sesiones expiradas...')
        
        result = InfrastructureCleanupService.cleanup_expired_sessions()
        
        self.stdout.write(
            self.style.SUCCESS(
                f'✅ Limpieza completada: {result["sessions"]} sesiones eliminadas'
            )
        )