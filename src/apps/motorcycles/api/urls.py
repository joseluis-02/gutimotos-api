# Django
from django.urls import path, include
# Routers local
from .routers import router


app_name = 'motorcycles_api'
urlpatterns = [
    # Endpoints adicionales
] + router
