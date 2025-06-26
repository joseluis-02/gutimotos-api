# Django
from django.urls import path, include
# App Productos
app_name = 'motorcycles_api'
# urls
urlpatterns = [
    # Motocicleta
    path("", include("apps.motorcycles.api.motorcycle.urls", namespace="motorcycle")),
    # Motocicleta Foto
    path("", include("apps.motorcycles.api.motorcycle_photo.urls", namespace="motorcycle_photo")),
]