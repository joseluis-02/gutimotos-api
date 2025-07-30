# urls.py
from django.urls import path
from .views import  ProductTabulatorTemplateView, ProductCatalogTemplateView, brand_options

app_name = 'web_product'

urlpatterns = [
    path('product/tabulator', ProductTabulatorTemplateView.as_view(), name='product_tabulator'),
    path('product/catalog', ProductCatalogTemplateView.as_view(), name='product_catalog'),
    # HTMX
    path('product/htmx/brand-options', brand_options, name='brand_options'),
    
]
