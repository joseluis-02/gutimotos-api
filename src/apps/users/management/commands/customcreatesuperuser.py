# miapp/management/commands/createsuperuser.py
from django.contrib.auth import get_user_model
from django.contrib.auth.management.commands.createsuperuser import Command as BaseCreateSuperuserCommand
from django.core.management import CommandError

class Command(BaseCreateSuperuserCommand):
    
    def add_arguments(self, parser):
        """
        Añadimos los argumentos personalizados para los campos adicionales,
        pero la solicitud será secuencial a través de `handle`.
        """
        super().add_arguments(parser)
        # Aquí no es necesario añadir nada si todo se solicita en `handle`
    def handle(self, *args, **options):
        # Obtenemos el modelo Usurio del sistema general
        User = get_user_model()
        # Obtenemos lista de atributos requeridos del usuario y agregamos nuestros atributos personalizados
        required_fields = User.REQUIRED_FIELDS + [
            'names',
            'paternal_surname',
            'maternal_surname',
            'document_code'
        ]
        # Creamos un objeto para estructurar el modelo usuario
        user_data = {}
        
        # Solicitar los campos en REQUIRED_FIELDS
        for field_name in required_fields:
            field_value = options.get(field_name)
            if not field_value:
                field_value = input(f'{field_name.capitalize()}: ')
                if not field_value:
                    raise CommandError(f'El campo {field_name} es obligatorio.')
            user_data[field_name] = field_value
        
        # En caso de que cuente con codigo de CI complemento
        document_complement = input(f'Document_complement (opcional): ')
        if (
            (len(document_complement.strip()) < 2 or 
            len(document_complement.strip())>5) and
            document_complement.strip()!=''
        ):
            raise CommandError(f'Codigo complemento es permitido de solo 2-5 caracteres')
        user_data['document_complement'] = document_complement.strip()
        
        # Solicitar el USERNAME_FIELD
        username_field = User.USERNAME_FIELD
        username_value = options.get(username_field)
        if not username_value:
            username_value = input(f'{username_field.capitalize()}: ')
            if not username_value:
                raise CommandError(f'El campo {username_field} es obligatorio.')
        user_data[username_field] = username_value
        
        # Solicitar la contraseña
        password = options.get('password')
        if not password:
            password = self.get_password()
        user_data['password'] = password
        
        # Crear el superusuario
        response = User.objects.create_superuser(**user_data)
        if response['created']:
            self.stdout.write(self.style.SUCCESS(f'Superusuario {user_data[username_field]} creado exitosamente.'))
        else:
            self.stderr.write(self.style.ERROR(f'No se pudo crear el superusuario {user_data[username_field]}.'))
        #super().handle(*args, **options)

    def get_password(self):
        from django.contrib.auth.management.commands.createsuperuser import getpass
        password = None
        password2 = None
        while password is None:
            password = getpass.getpass('Password: ')
            password2 = getpass.getpass('Password (again): ')
            if password != password2:
                self.stderr.write("Error: Las contraseñas no coinciden. Inténtalo de nuevo.")
                password = None
        return password
        super().handle(*args, **options)
    
    '''
    def ask(self, question):
        """
        Método para hacer una pregunta interactiva en la terminal, y devolver la respuesta.
        Si no se proporciona respuesta, se devuelve una cadena vacía.
        """
        while True:
            value = input(f"{question} ")
            if value.strip():
                return value
            else:
                print("Este campo no puede estar vacío. Por favor ingresa un valor válido.")
                
    '''