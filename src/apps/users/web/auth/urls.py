from django.urls import path
from .views import EmailAndPasswordLoginView, UserLogoutView

app_name = 'web_auth'

urlpatterns = [
    path("auth/email-password/", EmailAndPasswordLoginView.as_view(), name="auth_email_password"),
    path("auth/logout/", UserLogoutView.as_view(), name="auth_logout"),
]