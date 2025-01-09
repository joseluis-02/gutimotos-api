from django.urls import path
from .views import AuthTokenListView, login_or_refresh_token, render_invoices_view, create_or_validate_invoice, customer_list, items_list

urlpatterns = [
    path(
        'tokens/', 
        AuthTokenListView.as_view(), 
        name='list_tokens'
    ),
    path(
        'invoices/', 
        render_invoices_view, 
        name='list_invoices'
    ),
    path(
        'login/', 
        login_or_refresh_token, 
        name='login'
    ),
    path(
        'create/', 
        create_or_validate_invoice.as_view(), 
        name='create-validate'
    ),
    path(
        'customers/', 
        customer_list, 
        name='list_customers'
    ),
    path(
        'items/', 
        items_list, 
        name='list_customers'
    ),
]
