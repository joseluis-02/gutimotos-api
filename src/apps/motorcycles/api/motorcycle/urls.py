# Django
from django.urls import path, include
# Routers local
from .routers import motorcycle_tabulator

app_name = 'motorcycle'
urlpatterns = [
    # Routers
    path('', include(motorcycle_tabulator.urls)),
]
