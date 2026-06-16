from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.users'
    verbose_name = 'Usuarios'
    
    def ready(self):
        # Importar admin
        
        # Programar tareas
        from django.db.models.signals import post_migrate
        post_migrate.connect(self._schedule_tasks_handler, sender=self)
    
    def _schedule_tasks_handler(self, **kwargs):
        """Handler que se ejecuta después de migrate"""
        self._schedule_tasks()
    
    def _schedule_tasks(self):
        """Programa tareas de usuarios"""
        from django_q.models import Schedule
        
        # Limpiar tokens JWT expirados: cada día a las 3 AM
        Schedule.objects.update_or_create(
            func='apps.users.infrastructure.tasks.token_tasks.cleanup_expired_tokens_task',
            defaults={
                'name': 'Limpiar tokens JWT expirados',
                'schedule_type': Schedule.CRON,
                'cron': '0 3 * * *',
                'repeats': -1,
            }
        )
        # Limpiar OTPs expirados: cada día 4 AM
        Schedule.objects.update_or_create(
            func='apps.users.infrastructure.tasks.otp_tasks.cleanup_expired_otps_task',
            defaults={
                'name': 'Limpiar OTPs expirados',
                'schedule_type': Schedule.CRON,
                'cron': '0 4 * * *',
                'repeats': -1,
            }
        )