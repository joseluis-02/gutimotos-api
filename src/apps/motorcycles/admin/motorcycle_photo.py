# Django
from django.contrib import admin
# Model
from apps.motorcycles.models import MotorcyclePhoto

class PhotoAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'photo'
    ]
    search_fields = ['id', 'photo']
    ordering = ['-created']
    list_per_page = 10
    def delete_queryset(self, request, queryset):
        for obj in queryset:
            obj.delete()  # ← Aquí sí se llama tu delete personalizado

admin.site.register(MotorcyclePhoto,PhotoAdmin)