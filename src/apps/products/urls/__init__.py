# Django
from django.urls import path, include
# App Productos
app_name = 'products'
# urls
urlpatterns = [
    # Api V1
    path("api/", include("apps.products.urls.api", namespace="products_api")),
    # Web
    path("web/", include("apps.products.urls.web", namespace="products_web")),
]