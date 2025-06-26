# Django
from django.contrib import admin
# Models
from ..models import Product
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'code',
        'description',
        'brand',
        'measure',
        'country',
        'is_active',
    ]
    search_fields = ['code']
    ordering = ['-created']
    list_per_page = 10

admin.site.register(Product,ProductAdmin)