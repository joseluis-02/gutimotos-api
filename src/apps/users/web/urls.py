from django.urls import path, include

app_name = 'users_web'

urlpatterns = [
    path("auth/", include("apps.users.web.auth.urls", namespace="web_auth")),
    path("", include("apps.users.web.user.urls", namespace="web_user")),
]