# Django
from django.urls import path
# Views
from .views import WhatsAppRegisterView, WhatsAppVerifyView

app_name = 'api_user_whatsapp'
urlpatterns = [
    path("user-whatsapp/register/", WhatsAppRegisterView.as_view(), name="user_whatsapp_register"),
    path("user-whatsapp/verify/", WhatsAppVerifyView.as_view(), name="user_whatsapp_verify"),
]