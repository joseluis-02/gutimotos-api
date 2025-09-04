# Django
from django.urls import path
# Views
from .views import AuthGoogleAPIView, AuthLogoutAPIView, AuthRefreshTokenAPIView, TokenCleanupAPIView

app_name = 'api_auth'
urlpatterns = [
    path('auth/google/', AuthGoogleAPIView.as_view(), name='auth_google'),
    path('auth/logout/', AuthLogoutAPIView.as_view(), name='auth_logout'),
    path('auth/refresh-token/', AuthRefreshTokenAPIView.as_view(), name='auth_refresh_token'),
    path("auth/token-cleanup/", TokenCleanupAPIView.as_view(), name="auth_token_cleanup"),
]