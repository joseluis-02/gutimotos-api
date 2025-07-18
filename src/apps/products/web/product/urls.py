# urls.py
from django.urls import path
from .views import product_tabulator_json, ProductTabulatorTemplateView

app_name = 'web_product'

urlpatterns = [
    path('product/tabulator-json', product_tabulator_json, name='product_tabulator_json'),
    path('product/tabulator', ProductTabulatorTemplateView.as_view(), name='product_tabulator'),
]
