# Django
from django.contrib import admin
# Model
from apps.core.models import Currency

class CurrencyAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'name',
        'code',
        'symbol',
        'is_active',
    ]
    search_fields = ['name','code']
    ordering = ['-id']
    list_per_page = 10

admin.site.register(Currency,CurrencyAdmin)