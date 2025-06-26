# Django
from django.contrib import admin
# Models
from ..models import ProductPhoto

class ProductPhotoAdmin(admin.ModelAdmin):
    list_display = [
        'product__code', 
        'photo',
        'created',
        'modified'
    ]
    list_per_page = 10
    list_filter = ('created',)
    ordering = ['-created']
    search_fields = ['product__code']
    autocomplete_fields = ['product']
    #readonly_fields = ('created','modified',)

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            obj.delete()  # ← Aquí sí se llama tu delete personalizado
admin.site.register(ProductPhoto,ProductPhotoAdmin)