# Django
from django.contrib import admin
# Models
from ..models import ProductPrice
class ProductPriceAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'product__code',
        'currency__code',
        'base',
    ]
    search_fields = ['product__code', 'currency__code']
    list_filter = [
        'currency__code',
    ]
    ordering = ['-id']
    list_per_page = 10

admin.site.register(ProductPrice,ProductPriceAdmin)