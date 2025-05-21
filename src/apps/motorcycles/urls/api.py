# Django
from django.urls import path, include
# App Productos
app_name = 'motorcycles_api'
# urls
urlpatterns = [
    # Motocicleta Foto
    path("", include("apps.motorcycles.api.motorcycle_photo.urls", namespace="motorcycle_photo")),
    # Motocicleta Precio
    path("", include("apps.motorcycles.api.motorcycle_price.urls", namespace="motorcycle_price")),
]