# Django
from django.contrib import admin
# Model
from apps.motorcycles.models import Motorcycle

class MotorcycleAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'brand__name',
        'motorcycle_class__name',
        'motorcycle_type__name',
        'color__name',
        'country__name',
        'code_dim',
        'code_fvr',
        'model_year',
        'manufacturing_year',
        'code_chasis',
        'code_motor',
        'number_cc',
    ]
    search_fields = [
        'code_fvr',
        'code_dim',
        'code_chasis',
        'code_motor',
    ]
    list_filter = [
        'brand__name',
        'motorcycle_type__name',
        'color__name',
        'country__name',
    ]
    ordering = ['-model_year']
    list_per_page = 10

admin.site.register(Motorcycle,MotorcycleAdmin)