# Django
from django.urls import path, include
# Routers local
from .routers import router

app_name = 'motorcycle_photo'
urlpatterns = [
    # Endpoints adicionales
    path('', include(router.urls)),
]
