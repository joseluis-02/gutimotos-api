# Django
from django.contrib import admin
# Model
from apps.core.models import ExchangeRate

class ExchangeRateAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'from_currency__code',
        'to_currency__code',
        'rate',
        'updated_at',
        'is_active',
    ]
    search_fields = ['to_currency__code']
    ordering = ['-updated_at']
    list_per_page = 10

admin.site.register(ExchangeRate,ExchangeRateAdmin)