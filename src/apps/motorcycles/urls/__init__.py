# Django
from django.urls import path, include
# App Productos
app_name = 'motorcycles'
# urls
urlpatterns = [
    # Api V1
    path("api/", include("apps.motorcycles.urls.api", namespace="motorcycles_api")),
    # Web V1
    path("", include("apps.motorcycles.urls.web", namespace="motorcycles_web")),
]