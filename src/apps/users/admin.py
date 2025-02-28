# Django
from django.contrib import admin
# Models local
from .models import User, UserProfile

# Registrando al modelo User=Usuario
admin.site.register(User)
# Registrando al modelo UserProfile=PerfilUsuario
admin.site.register(UserProfile)