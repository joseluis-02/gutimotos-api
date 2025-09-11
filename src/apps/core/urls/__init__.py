# Django
from django.urls import path, include
# App Productos
app_name = 'core'
# urls
urlpatterns = [
    # Api
    path("api/", include("apps.core.urls.api", namespace="core_api")),
]