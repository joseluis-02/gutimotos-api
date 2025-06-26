# Django
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

class DashboardIndexView(LoginRequiredMixin, TemplateView):
    template_name = 'admin/pages/blank.html'
    login_url = 'users:users_web:web_auth:auth_email_password'  # URL de inicio de sesión