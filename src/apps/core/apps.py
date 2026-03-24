from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.core'
    verbose_name = 'Core'
    
    def ready(self):
        """Inicialización de la app"""
        # Programar tareas de limpieza
        from django.db.models.signals import post_migrate
        post_migrate.connect(self._schedule_cleanup_tasks, sender=self)
    
    def _schedule_cleanup_tasks(self, **kwargs):
        """Programa tareas de limpieza de infraestructura"""
        from django_q.models import Schedule
        
        # Limpiar sesiones Django: diario 2 AM
        Schedule.objects.update_or_create(
            func='apps.core.infrastructure.tasks.cleanup_tasks.cleanup_django_sessions_task',
            defaults={
                'name': 'Limpiar sesiones Django expiradas',
                'schedule_type': Schedule.CRON,
                'cron': '0 2 * * *',
                'repeats': -1,
            }
        )