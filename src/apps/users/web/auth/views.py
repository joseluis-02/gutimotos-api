# Django
from django.contrib.auth.views import LoginView
from django.views import View
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.utils.http import url_has_allowed_host_and_scheme
from django.shortcuts import resolve_url
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
# Forms
from .forms import UserLoginForm

class EmailAndPasswordLoginView(LoginView):
    template_name = 'users/auth/pages/sign_in.html'
    authentication_form = UserLoginForm
    redirect_authenticated_user = True

    def form_valid(self, form):
        return super().form_valid(form)

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={self.request.get_host()}):
            return next_url
        return resolve_url('dashboard:index')

@method_decorator(never_cache, name='dispatch')
class UserLogoutView(View):
    def dispatch(self, request, *args, **kwargs):
        # Cierra la sesión de forma segura
        logout(request)
        request.session.flush()

        # Redirige de forma explícita
        response = redirect('/')

        # Evita volver atrás con la flecha del navegador
        response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'

        return response