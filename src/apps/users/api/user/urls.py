# Django
from django.urls import path, include
# Views
from .views import UserCreateAPIView, UserUpdateAPIView, UserListAPIView

app_name = 'api_user'
urlpatterns = [
    # List User
    path(
        'list',
        UserListAPIView.as_view(),
        name='api_user_list'
    ),
    # Create User
    path(
        'create',
        UserCreateAPIView.as_view(),
        name='api_user_create'
    ),
    # Update User
    path(
        'update',
        UserUpdateAPIView.as_view(),
        name='api_user_update'
    ),
]
