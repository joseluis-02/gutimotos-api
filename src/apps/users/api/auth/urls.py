# Django
from django.urls import path, include
# Views
from .views import LoginEmailAndPasswordAPIView, LoginGoogleAPIView, LogoutAPIView

app_name = 'api_auth'
urlpatterns = [
    # Emial/password login
    path(
        'email-password',
        LoginEmailAndPasswordAPIView.as_view(),
        name='auth_email_password'
    ),
    # Google login
    path(
        'google',
        LoginGoogleAPIView.as_view(),
        name='auth_google'
    ),
    # Logout
    path(
        'logout', 
        LogoutAPIView.as_view(), 
        name='auth_logout'
    ),
]