# Django
from django.urls import path, include
# Routers local
from .routers import router_urls

app_name = 'product_photo'
urlpatterns = [
    # Endpoints adicionales
]+ router_urls
