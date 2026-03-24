# quotations/urls.py
from django.urls import path
from .views import create_quotation, patch_quotation_status, update_quotation_items
app_name = 'quotation'
urlpatterns = [
    path('api/quotation/create/', create_quotation, name='create_quotation'),
    path('api/quotation/patch-status/<uuid:quotation_id>/', patch_quotation_status, name='patch_quotation_status'),
    path('api/quotation/update-items/<uuid:quotation_id>/', update_quotation_items, name='update_quotation_items'),
]
