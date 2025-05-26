from django.urls import path, include

app_name = 'users_api'

urlpatterns = [
    path("auth/", include("apps.users.api.auth.urls", namespace="api_auth")),
    path("", include("apps.users.api.user.urls", namespace="api_user")),
]