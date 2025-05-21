# Django
from django.views import View
from django.contrib.auth import logout
from django.shortcuts import redirect

# View logout
class UserLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('users_web:web_auth:web_auth_email_password')  # O la URL que desees