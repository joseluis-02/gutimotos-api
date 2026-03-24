# Django
from django.contrib import admin
# Users - Infrastructure
from apps.users.infrastructure.persistence.models.otp import OTP


@admin.register(OTP)
class OTPAdmin(admin.ModelAdmin):
    """Admin para OTPs"""
    
    list_display = [
        'email',
        'code',
        'is_used',
        'attempts',
        'created',
        'expired',
        'is_expired'
    ]
    
    list_filter = [
        'is_used',
        'created',
        'expired'
    ]
    
    search_fields = [
        'email',
        'code'
    ]
    
    readonly_fields = [
        'id',
        'email',
        'code',
        'created',
        'expired',
        'is_used',
        'attempts'
    ]
    
    ordering = ['-created']
    
    date_hierarchy = 'created'
    
    def is_expired(self, obj):
        """Indica si el OTP está expirado"""
        from django.utils import timezone
        return timezone.now() > obj.expired
    is_expired.boolean = True
    is_expired.short_description = 'Expirado'
    
    def has_add_permission(self, request):
        """No permitir crear OTPs desde admin"""
        return False
    
    def has_change_permission(self, request, obj=None):
        """No permitir editar OTPs"""
        return False