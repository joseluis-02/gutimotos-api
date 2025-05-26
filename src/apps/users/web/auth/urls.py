from django.urls import path
from .views import UserLoginFormView, UserLogoutView

app_name = 'web_auth'

urlpatterns = [
    path("email-password/", UserLoginFormView.as_view(), name="web_auth_email_password"),
    path("logout/", UserLogoutView.as_view(), name="web_auth_logout"),
]