from django import forms

class LoginOrRefreshTokenForm(forms.Form):
    # Opción para elegir entre iniciar sesión o refrescar token
    ACTION_CHOICES = [
        ('password', 'Iniciar sesión con contraseña'),
        ('refresh_token', 'Refrescar token')
    ]
    """
    action = forms.ChoiceField(
        choices=ACTION_CHOICES, 
        widget=forms.Select(
            attrs={
                'class': 'form-select mb-2',
                'aria-label': 'Opcion de obtener'
        }), 
        label="Seleccionar acción",
    )
    """
    
    # Campo para el correo electrónico
    email = forms.EmailField(
        max_length=100, 
        required=True, 
        label="Correo electrónico",
        widget=forms.EmailInput(
            attrs={
                'class':'form-control',
                'placeholder':'Ingrese email'
            }
        )
    )
    
    # Campo para la contraseña
    password = forms.CharField(
        max_length=100, 
        widget=forms.PasswordInput(
            attrs={
                'placeholder':'Ingrese password',
                'class': 'form-control ',
                'aria-describedby': 'passwordHelpBlock'
            }
        ), 
        required=True,
        label="Contraseña",
    )
