# Django
from django.urls import path, include
# App Productos
app_name = 'products_web'
# urls
urlpatterns = [
    # Product
    path("", include("apps.products.web.product.urls", namespace="web_product")),
]