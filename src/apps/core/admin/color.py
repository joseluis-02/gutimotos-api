# Django
from django.contrib import admin
# Model
from apps.core.models import Color

class ColorAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'name',
        'code_hex',
        'is_active',
    ]
    search_fields = ['name','code_hex']
    ordering = ['-id']
    list_per_page = 10

admin.site.register(Color,ColorAdmin)