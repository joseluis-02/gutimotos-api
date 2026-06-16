# Django
from django.core.management.base import BaseCommand
# Django-Q2
from django_q.tasks import schedule
from django_q.models import Schedule

class Command(BaseCommand):
    help = 'Configura tareas programadas para users'

    def handle(self, *args, **options):
        
        # Limpiar tokens - Medianoche
        schedule(
            'users.tasks.cleanup.run_all_token_cleanup_tasks',
            name='[USERS] Limpiar tokens expirados',
            schedule_type=Schedule.CRON,
            cron='0 0 * * *',
            repeats=-1,
        )
        self.stdout.write(self.style.SUCCESS('✓ Limpiar tokens (00:00)'))
        
        # Limpiar sesiones - 00:30
        schedule(
            'users.tasks.cleanup.limpiar_sesiones_expiradas',
            name='[USERS] Limpiar sesiones',
            schedule_type=Schedule.CRON,
            cron='30 0 * * *',
            repeats=-1,
        )
        self.stdout.write(self.style.SUCCESS('✓ Limpiar sesiones (00:30)'))