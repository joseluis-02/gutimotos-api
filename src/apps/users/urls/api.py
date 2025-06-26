# Django
from django.urls import path, include
# App Productos
app_name = 'users_api'
# urls
urlpatterns = [
    # Auth 
    path("", include("apps.users.api.auth.urls", namespace="api_auth")),
]