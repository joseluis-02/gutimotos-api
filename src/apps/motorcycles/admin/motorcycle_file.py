# Django
from django.contrib import admin
# Model
from apps.motorcycles.models import MotorcycleFile

class MotorcycleFileAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'brand_name',
        'motorcycle_type_path',
        'color_name',
        'is_active'
    ]
    def brand_name(self, obj):
        return obj.brand.name
    brand_name.short_description = 'MARCA'
    def motorcycle_type_path(self, obj):
        return obj.motorcycle_type.get_full_path()
    motorcycle_type_path.short_description = 'TIPO DE MOTOCICLETA'
    def color_name(self, obj):
        return obj.color.name
    color_name.short_description = 'COLOR'
    search_fields = ['brand__name', 'motorcycle_type__name', 'color__name']
    list_filter = [
        'brand__name',
        'motorcycle_type__name',
        'color__name',
    ]
    list_per_page = 10

admin.site.register(MotorcycleFile,MotorcycleFileAdmin)