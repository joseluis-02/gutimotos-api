# Django
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
# Forms
from ..forms import UserRegisterForm
# Models
from ....models import User

class UserRegisterFormView(FormView):
    template_name = 'auth/register.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:auth_login')

    # Para que un FormView funcione, necesita de la función form_valid
    def form_valid(self, form):
        # Crear el usuario
        User.objects.create_user(
            form.cleaned_data['email'],
            form.cleaned_data['password1'],
        )
        # Enviar un correo de bienvenida
        return super(UserRegisterFormView, self).form_valid(form)
