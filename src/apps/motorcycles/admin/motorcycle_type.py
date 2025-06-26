# Django
from django.contrib import admin
# Model
from apps.motorcycles.models import MotorcycleType

class MotorcycleTypeAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'name',
        'get_full_path',
        'is_subtype',
    ]
    search_fields = ['name']
    list_per_page = 10

admin.site.register(MotorcycleType,MotorcycleTypeAdmin)