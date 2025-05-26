# Django
from django.urls import path, include
# App Productos
app_name = 'products_api'
# urls
urlpatterns = [
    path("product/", include("apps.products.api.product.urls", namespace="api_product")),
    path("product-photo/", include("apps.products.api.product_photo.urls", namespace="api_product_photo")),
]