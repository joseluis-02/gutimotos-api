# Django
from django.contrib import admin
# Model
from apps.core.models import TypePrice

class TypePricepeAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'name',
        'slug',
        'profit_margin',
        'is_active',
    ]
    search_fields = ['name','slug']
    ordering = ['-id']
    list_per_page = 10

admin.site.register(TypePrice,TypePricepeAdmin)