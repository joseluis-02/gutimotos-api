# Django
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

class DashboardIndexView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/index.html'
    login_url = 'users:auth_login'  # URL de inicio de sesión