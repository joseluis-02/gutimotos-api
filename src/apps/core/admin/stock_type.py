# Django
from django.contrib import admin
# Model
from apps.core.models import StockType

class StockTypeAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'name',
        'slug',
        'get_stock_transaction_display',
        'is_active',
    ]
    def get_stock_transaction_display(self, obj):
        return "Entrada" if obj.stock_transaction else "Salida"
    get_stock_transaction_display.short_description = 'Transacción de stock'
    search_fields = ['name','slug']
    ordering = ['-id']
    list_per_page = 10

admin.site.register(StockType,StockTypeAdmin)