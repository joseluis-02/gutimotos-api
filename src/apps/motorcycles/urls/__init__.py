# Django
from django.urls import path, include
# App Productos
app_name = 'motorcycles'
# urls
urlpatterns = [
    # Api V1
    path("api/", include("apps.motorcycles.urls.api", namespace="product")),
]