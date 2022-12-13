from django.db import models
from .managers import CustomUserManager
from django.contrib.auth.models import (
    AbstractUser, PermissionsMixin
)


# Create your models here.

class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(verbose_name='email address',
                              max_length=255,
                              unique=True)
    USERNAME_FIELD = 'email'

    objects = CustomUserManager()

    def __str__(self):
        return self.email
