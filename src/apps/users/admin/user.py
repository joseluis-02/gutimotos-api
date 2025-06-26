# Django
from django.contrib import admin
# Models
from ..models import User
class UserAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'email',
        'email_verified',
        'is_staff',
        'is_active',
    ]
    search_fields = ['email']
    ordering = ['-id']
    list_per_page = 10

admin.site.register(User,UserAdmin)