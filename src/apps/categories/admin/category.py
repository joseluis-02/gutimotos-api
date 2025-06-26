# Django
from django.contrib import admin
# Model
from ..models.category import Category

class CategoryAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'code_sin',
        'description_sin',
        'economic_activity',
        'is_active',
    ]
    search_fields = ['code_sin']
    list_per_page = 10

admin.site.register(Category,CategoryAdmin)