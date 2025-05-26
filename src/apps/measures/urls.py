from django.urls import path
from .views import hx_measure_card_list, hx_measure_detail

app_name = 'measures'

urlpatterns = [
    path("", hx_measure_card_list, name="hx_measure_card_list"),
    path('<int:pk>/', hx_measure_detail, name='hx_measure_detail'),
]