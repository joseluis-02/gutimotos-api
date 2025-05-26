# Django
from django.urls import path
# Views
from .views import MotorcycleMultiCurrencyPriceAPIView

app_name = 'motorcycle_price'
urlpatterns = [
    path(
        "motorcycle-price/multi-currency", 
        MotorcycleMultiCurrencyPriceAPIView.as_view(), 
        name="list"
    ),
]