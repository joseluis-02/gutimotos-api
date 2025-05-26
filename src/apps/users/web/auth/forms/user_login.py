# Dajngo
from django import forms
from django.contrib.auth import authenticate
# Models
from ....models import User

class UserLoginForm(forms.Form):
    email = forms.EmailField(
        required=True
    )
    password = forms.CharField(
        required=True
    )

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        user = authenticate(email=email, password=password)
        if user is None:
            raise forms.ValidationError("Credenciales inválidas")
        if not user.is_active:
            raise forms.ValidationError("Usuario inactivo")

        self.user = user  # <- ESTO es clave
        return cleaned_data
