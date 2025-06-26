# Django
from django.contrib import admin
# Moodel
from ..models.economic_activity import EconomicActivity

class EconomicActivityAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'code_sin',
        'description_sin',
        'is_primary',
        'is_active',
    ]
    search_fields = ['code_sin']
    list_per_page = 10
admin.site.register(EconomicActivity, EconomicActivityAdmin)