# Django
from django.contrib import admin
# Model
from apps.motorcycles.models import TransmissionType

class TransmissionTypeAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'name',
        'is_active',
    ]
    search_fields = ['name']
    list_per_page = 10

admin.site.register(TransmissionType,TransmissionTypeAdmin)