# Django
from django.urls import path
# Views
from .views import ProductListAPIView
# App name
app_name = 'api_product'
# Urls
urlpatterns = [
    path(
        '',
        ProductListAPIView.as_view(),
        name='list'
    ),
]