# Django
from django.urls import path, include
# App Productos
app_name = 'users'
# urls
urlpatterns = [
    # Web v1
    path("", include("apps.users.urls.web", namespace="users_web")),
    # Api v1
    path("api/", include("apps.users.urls.api", namespace="users_api")),
]