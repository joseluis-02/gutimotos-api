from django.apps import AppConfig


class QuotationsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.quotations'
    verbose_name = 'Cotizaciones'
    
    # Cargar admin
    def ready(self):
        import apps.quotations.presentation.admin
        # Registrar signal para programar tareas después de migrate
        from django.db.models.signals import post_migrate
        post_migrate.connect(self._schedule_tasks_handler, sender=self)
    
    def _schedule_tasks_handler(self, **kwargs):
        """Handler que se ejecuta después de migrate"""
        self._schedule_tasks()
    '''
    # Production
    def _schedule_tasks(self):
        """Programa tareas recurrentes"""
        from django_q.models import Schedule
        
        # 1. Expirar cotizaciones cada 1 hora
        Schedule.objects.update_or_create(
            func='core.tasks.quotation_tasks.expire_quotations_task',
            defaults={
                'name': 'Expirar cotizaciones vencidas',
                'schedule_type': Schedule.HOURLY,
                'repeats': -1,
            }
        )
        
        # 2. Limpiar canceladas cada día a las 2 AM
        Schedule.objects.update_or_create(
            func='core.tasks.quotation_tasks.cleanup_cancelled_quotations_task',
            defaults={
                'name': 'Limpiar cotizaciones canceladas',
                'schedule_type': Schedule.CRON,
                'cron': '0 2 * * *',  # 2 AM todos los días
                'repeats': -1,
            }
        )
        
        # 3. Limpiar expiradas antiguas cada día a las 3 AM
        Schedule.objects.update_or_create(
            func='core.tasks.quotation_tasks.cleanup_old_expired_quotations_task',
            defaults={
                'name': 'Limpiar cotizaciones expiradas antiguas',
                'schedule_type': Schedule.CRON,
                'cron': '0 3 * * *',  # 3 AM todos los días
                'repeats': -1,
            }
        )
        # 4. Notificar expiración cada 6 horas
        Schedule.objects.update_or_create(
            func='apps.core.tasks.quotation_tasks.notify_expiring_quotations_task',
            defaults={
                'name': 'Notificar cotizaciones próximas a expirar',
                'schedule_type': Schedule.MINUTES,
                'minutes': 360,  # Cada 6 horas
                'repeats': -1,
            }
        )
    '''

    def _schedule_tasks(self):
        """Tareas cada pocos minutos - MODO PRUEBA"""
        from django_q.models import Schedule
        
        # Expirar: cada 2 minutos
        Schedule.objects.update_or_create(
            func='apps.quotations.infrastructure.tasks.quotation_tasks.expire_quotations_task',
            defaults={
                'name': 'Expirar cotizaciones',
                'schedule_type': Schedule.MINUTES,
                'minutes': 5,
                'repeats': -1,
            }
        )
        
        # Limpiar canceladas: cada 5 minutos
        Schedule.objects.update_or_create(
            func='apps.quotations.infrastructure.tasks.quotation_tasks.cleanup_cancelled_quotations_task',
            defaults={
                'name': 'Limpiar canceladas',
                'schedule_type': Schedule.CRON,
                'cron': '0 2 * * *',  # 2 AM todos los días
                'repeats': -1,
            }
        )
        
        # Limpiar expiradas antiguas: cada 5 minutos
        Schedule.objects.update_or_create(
            func='apps.quotations.infrastructure.tasks.quotation_tasks.cleanup_old_expired_quotations_task',
            defaults={
                'name': 'Limpiar expiradas antiguas',
                'schedule_type': Schedule.MINUTES,
                'minutes': 30,
                'repeats': -1,
            }
        )
        
        # Notificar: cada 3 minutos
        Schedule.objects.update_or_create(
            func='apps.quotations.infrastructure.tasks.quotation_tasks.notify_expiring_quotations_task',
            defaults={
                'name': 'Notificar expiración',
                'schedule_type': Schedule.MINUTES,
                'minutes': 5,
                'repeats': -1,
            }
        )