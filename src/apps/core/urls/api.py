# Django
from django.urls import path, include
# App Productos
app_name = 'core_api'
# urls
urlpatterns = [
    # Brand
    path("", include("apps.core.api.brand.urls", namespace="brand")),
    # Color
    path("", include("apps.core.api.color.urls", namespace="color")),
    # Currency
    path("", include("apps.core.api.currency.urls", namespace="currency")),
    # Type price
    path("", include("apps.core.api.type_price.urls", namespace="type_price")),
]