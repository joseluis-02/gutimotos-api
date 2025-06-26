# Django
from django.contrib import admin
# Model
from ..models.measure import Measure

class MeasureAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'code_sin',
        'short_name',
        'name',
        'is_active',
    ]
    search_fields = ['code_sin']
    list_per_page = 10

admin.site.register(Measure,MeasureAdmin)