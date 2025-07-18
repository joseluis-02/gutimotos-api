# Django
from django.urls import path
# Views
from .views import ProductListAPIView, ProductTabulatorListAPIView
# App name
app_name = 'api_product'
# Urls
urlpatterns = [
    path(
        'product/list',
        ProductListAPIView.as_view(),
        name='list'
    ),
    path(
        'product/tabulator',
        ProductTabulatorListAPIView.as_view(),
        name='product_tabulator'
    ),
]