from django.urls import path
from .views import UserRegisterFormView

app_name = 'web_user'

urlpatterns = [
    path("register/", UserRegisterFormView.as_view(), name="web_user_register"),
]