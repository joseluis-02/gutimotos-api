# Django
from django.urls import path
# Views
from .views import BrandTemplateView

app_name = 'motorcycles'
urlpatterns = [
    path(
        'brand/list/',
        BrandTemplateView.as_view(),
        name='brand-list'
    ),
]
