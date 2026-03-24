# Django
from django.contrib import admin
# Models
from ..models import UserWhatsApp
class UserWhatsAppAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'country_code',
        'number',
        'full_number',
        'verified',
        'otp_signed',
        'otp_expires_at',
        'created',
        'user_email'
    ]
    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = "Email del Usuario"
    search_fields = ['number']
    ordering = ['-id']
    list_per_page = 10

admin.site.register(UserWhatsApp,UserWhatsAppAdmin)