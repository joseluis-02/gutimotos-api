# Django
from django.contrib import admin
# Models
from ..models import ProductStock
class ProductStockAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'product__code',
        'stock_type__name',
        'quantity',
    ]
    search_fields = ['product__code']
    list_filter = [
        'stock_type__name',
    ]
    ordering = ['-id']
    list_per_page = 10

admin.site.register(ProductStock,ProductStockAdmin)