# Django
from django.urls import path, include
# App Productos
app_name = 'users_web'
# urls
urlpatterns = [
    # Motocicleta Foto
    path("", include("apps.users.web.auth.urls", namespace="web_auth")),
]