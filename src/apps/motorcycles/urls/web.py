# Django
from django.urls import path, include
# App Productos
app_name = 'motorcycles_web'
# urls
urlpatterns = [
    # Motocicleta Foto
    path("", include("apps.motorcycles.web.motorcycle_photo.urls", namespace="web_motorcycle_photo")),
    # Motocicleta
    path("", include("apps.motorcycles.web.motorcycle.urls", namespace="web_motorcycle")),
]