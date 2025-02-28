# Python
from uuid import UUID, uuid4
# Django
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

# Apps de terceros -> Model utils
from model_utils.models import TimeStampedModel

# Models local
from apps.persons.models import NaturalPerson

# Managers
from .managers import UserMenager

# Model User
class User(AbstractBaseUser,PermissionsMixin,TimeStampedModel):
    id:UUID = models.UUIDField(
        primary_key=True,
        null=False,
        blank=False,
        default=uuid4,
        editable=False
    )
    email:str = models.EmailField(
        max_length=255,
        unique=True,
        verbose_name='Correo electrónico'
    )
    is_staff = models.BooleanField(
        default=False
    )
    is_active = models.BooleanField(
        default=False
    )
    objects = UserMenager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    # Functions
    def __str__(self):
        return f'{self.email}'

# Modelo Perfil de usuario
class UserProfile(models.Model):
    natural_person = models.OneToOneField(
        NaturalPerson,
        on_delete=models.CASCADE,
        related_name='up_natural_person',
        null=False,
        blank=False,
        verbose_name="Persona asociada"
    )
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='up_user',
        null=False,
        blank=False,
        verbose_name="Usuario asociada"
    )
    # foto de perfil
    def __str__(self):
        return f'{self.natural_person} {self.user}'
