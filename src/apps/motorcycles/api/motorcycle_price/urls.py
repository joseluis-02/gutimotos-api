# Django
from django.urls import path, include
# Views
from .views import MotorcyclePricesByMotorcycleTypeAPIView

app_name = 'motorcycle_price'
urlpatterns = [
    path(
        "motorcycle-price/<int:motorcycle_type_id>/<slug:type_price_slug>",
        MotorcyclePricesByMotorcycleTypeAPIView.as_view(),
        name="motorcycle_price_by_motorcycle_type_and_type_price_slug",
    ),
]