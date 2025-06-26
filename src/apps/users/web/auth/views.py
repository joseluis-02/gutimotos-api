# Django
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django.utils.http import url_has_allowed_host_and_scheme
from django.shortcuts import resolve_url
# Forms
from .forms import UserLoginForm

class EmailAndPasswordLoginView(LoginView):
    template_name = 'users/auth/pages/sign_in.html'
    authentication_form = UserLoginForm
    redirect_authenticated_user = True

    def form_valid(self, form):
        user = form.get_user()
        #messages.success(self.request, f'¡Bienvenido, {user.email}!')
        return super().form_valid(form)

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={self.request.get_host()}):
            return next_url
        return resolve_url('dashboard:index')

class UserLogoutView(LogoutView):
    next_page = 'users:users_web:web_auth:auth_email_password'  # o usa get_next_page() si necesitas lógica adicional
    def dispatch(self, request, *args, **kwargs):
        #messages.success(request, "Has cerrado sesión correctamente.")
        # Limpiar cualquier dato extra en sesión si necesitas
        request.session.flush()
        return super().dispatch(request, *args, **kwargs)