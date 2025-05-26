# Django
from django.shortcuts import redirect
from django.views.generic.edit import FormView

from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
# Forms
from ..forms import UserLoginForm

# FormView para el inicio de sesión
class UserLoginFormView(FormView):
    template_name = 'auth/login.html'
    form_class = UserLoginForm
    success_url = reverse_lazy('dashboard:index')
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard:index')  # Redirige al dashboard si el usuario ya está autenticado
        return super().dispatch(request, *args, **kwargs)
    def form_valid(self, form):
        # Autenticar al usuario
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        user = authenticate(self.request, email=email, password=password)
        if user is not None:
            if user.is_active:
                login(self.request, user)  # Iniciar sesión y guardar en la sesión
                # Redirigir al valor de 'next' si está presente
                next_url = self.request.POST.get('next') or self.request.GET.get('next')
                if next_url:
                    return HttpResponseRedirect(next_url)
                return super().form_valid(form)
            else:
                form.add_error(None, 'Usuario inactivo')
                return super().form_invalid(form)
        else:
            form.add_error(None, 'Credenciales incorrectas')
            return super().form_invalid(form)
