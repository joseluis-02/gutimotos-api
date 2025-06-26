# Django
from django.contrib import admin
# Model
from apps.motorcycles.models import MotorcycleClass

class MotorcycleClassAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'slug',
        'name',
    ]
    search_fields = ['slug']
    ordering = ['-id']
    list_per_page = 10

admin.site.register(MotorcycleClass,MotorcycleClassAdmin)