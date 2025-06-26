# Django
from django.contrib import admin
# Model
from apps.motorcycles.models import MotorcyclePrice

class MotorcyclePriceAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'brand_name',
        'motorcycle_type_path',
        'currency_name',
        'base',
    ]
    def brand_name(self, obj):
        return obj.brand.name
    brand_name.short_description = 'MARCA'
    def motorcycle_type_path(self, obj):
        return obj.motorcycle_type.get_full_path()
    motorcycle_type_path.short_description = 'TIPO DE MOTOCICLETA'
    def currency_name(self, obj):
        return obj.currency.name
    currency_name.short_description = 'MONEDA'
    search_fields = ['brand__name']
    list_per_page = 10

admin.site.register(MotorcyclePrice,MotorcyclePriceAdmin)