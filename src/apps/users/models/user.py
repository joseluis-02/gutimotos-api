# Python
from uuid import UUID, uuid4
# Django
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
# Apps de terceros -> Model utils
from model_utils.models import TimeStampedModel
# Managers
from ..managers.user import UserMenager
"""
AbstractBaseUser me proporciona la funcionalidad básica de un usuario, como la autenticación y la gestión de contraseñas.
Propiedad / Método	Descripción
is_authenticated	True si el usuario está autenticado.
set_password(raw_password)	Hashea y guarda una contraseña segura.
check_password(raw_password)	Verifica una contraseña contra la hasheada.
get_username()	Devuelve el identificador único del usuario (USERNAME_FIELD).
last_login	Fecha/hora del último inicio de sesión (si se guarda).
"""

"""
PermissionsMixin me proporciona la funcionalidad de permisos y grupos.
Propiedad / Método	Descripción
is_superuser	Indica si el usuario tiene todos los permisos.
groups	Relación con grupos de permisos.
user_permissions	Relación directa con permisos individuales.
has_perm(perm)	Devuelve True si el usuario tiene un permiso.
has_perms(perms_list)	Verifica múltiples permisos.
has_module_perms(app_label)	Verifica permisos sobre una app.
"""
# Model User
class User(AbstractBaseUser,PermissionsMixin,TimeStampedModel):
    id:UUID = models.UUIDField(
        primary_key=True,
        null=False,
        blank=False,
        default=uuid4,
        editable=False
    )
    auth_uid = models.CharField(
        max_length=128,
        unique=True,
        null=True,
        blank=True,
        verbose_name="Identificador del proveedor de autenticación"
    )
    email:str = models.EmailField(
        max_length=255,
        unique=True,
        verbose_name='Correo electrónico'
    )
    email_verified:bool = models.BooleanField(
        default=False,
        verbose_name='Estado de verificación del correo electrónico'
    )
    auth_provider = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name="Proveedor de autenticación"
    )
    is_staff = models.BooleanField(
        default=False
    )
    is_active = models.BooleanField(
        default=False
    )
    # Manager
    objects = UserMenager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    # Meta
    class Meta:
        indexes = [
            models.Index(fields=['created']),
        ]
    # Functions
    def __str__(self):
        return f'{self.email}'