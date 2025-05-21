# Django
from django.urls import path
# Views
from .views import ProductPhotoListAPIView
# App name
app_name = 'api_product_photo'
# Urls
urlpatterns = [
    path(
        '',
        ProductPhotoListAPIView.as_view(),
        name='list'
    ),
]