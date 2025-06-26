# Django
from django.contrib import admin
# Model
from apps.core.models import Country

class CountryAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'name',
        'code',
        'is_active',
    ]
    search_fields = ['name','code']
    ordering = ['-id']
    list_per_page = 10

admin.site.register(Country,CountryAdmin)