# Django
from django.contrib import admin
# Model
from apps.core.models import Brand

class BrandAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'name',
        'is_active',
    ]
    search_fields = ['name']
    ordering = ['-id']
    list_per_page = 10

admin.site.register(Brand,BrandAdmin)