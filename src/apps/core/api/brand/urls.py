# Django
from django.urls import path, include
# Routers local
from .routers import router_urls

app_name = 'brand'
urlpatterns = [
] + router_urls
