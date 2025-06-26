# Dajngo
from django import forms
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
# Models
from ...models import User

class UserLoginForm(forms.Form):
    email = forms.EmailField(
        label='Correo electrónico',
        widget=forms.EmailInput(attrs={
            'placeholder': 'ejemplo@gmail.com',
            'class': 'form-control form-control-lg',
            'autocomplete': 'email',
        }),
        error_messages={
            'required': 'El correo electrónico es obligatorio.',
            'invalid': 'Ingrese una dirección de correo válida.',
        }
    )
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'tu contraseña',
            'class': 'form-control form-control-lg',
            'autocomplete': 'current-password',
        }),
        error_messages={
            'required': 'La contraseña es obligatoria.',
        }
    )
    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)

    def clean_email(self):
        """Normaliza y valida existencia del email"""
        email = self.cleaned_data.get('email', '').strip().lower()
        if not User.objects.filter(email=email).exists():
            raise ValidationError("Este correo electrónico no está registrado.")
        return email

    def clean_password(self):
        """Valida que la contraseña no esté vacía"""
        password = self.cleaned_data.get('password', '').strip()
        if not password:
            raise ValidationError("La contraseña es obligatoria.")
        return password

    def clean(self):
        """Validación completa de credenciales"""
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        if not email or not password:
            return cleaned_data  # No seguir si ya hay errores previos

        user = User.objects.filter(email=email).first()
        if not user:
            # Esto rara vez se ejecuta gracias a `clean_email`, pero lo dejamos por seguridad
            self._errors['custom_error'] = self.error_class(["Las credenciales proporcionadas no son válidas."])
            return cleaned_data

        if not user.is_active:
            self._errors['custom_error'] = self.error_class(["Usuario inactivo, contacte al administrador."])
            return cleaned_data

        authenticated_user = authenticate(self.request, email=email, password=password)
        if authenticated_user is None:
            self.add_error('password', "La contraseña es incorrecta.")
            return cleaned_data

        self.user_cache = authenticated_user
        return cleaned_data

    def get_user(self):
        """Retorna el usuario autenticado, si está disponible"""
        return getattr(self, 'user_cache', None)