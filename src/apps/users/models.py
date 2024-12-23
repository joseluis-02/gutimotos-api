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
    natural_person = models.OneToOneField(
        NaturalPerson,
        on_delete=models.CASCADE,
        related_name='user',
        null=False,
        blank=False,
        verbose_name="Persona asociada"
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
    