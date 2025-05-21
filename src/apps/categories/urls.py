from django.urls import path
from .views import hx_category_card_list, hx_category_list_table, hx_category_detail

app_name = 'categories'

urlpatterns = [
    path("", hx_category_card_list, name="hx_category_card_list"),
    path('<int:pk>/', hx_category_detail, name='hx_category_detail'),
]