from django.db import models
from .managers import CustomUserManager
from django.utils.safestring import mark_safe
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import (
    AbstractUser
)


# Create your models here.

class UserProfile(AbstractUser):
    username = None
    image = models.ImageField(upload_to='user/images',
                              null=True,
                              blank=True)
    email = models.EmailField(verbose_name='email address',
                              max_length=255,
                              unique=True)
    phone_number = models.CharField(max_length=80)
    address = models.CharField(max_length=120, null=True, blank=True)
    bio = models.TextField(max_length=400,
                           null=True,
                           blank=True)
    is_manager = models.BooleanField(default=False)

    objects = CustomUserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def get_full_name(self):
        if not self.first_name and not self.last_name:
            return self.username
        else:
            return "%s %s" % (self.first_name, self.last_name)

    def image_tag(self):
        if self.image:
            return mark_safe(f'<a href="{self.image.url}"><img src="{self.image.url}" style="height:40px;"/></a>')
        return 'no_image'

    @property
    def image_url(self):
        if self.image:
            if settings.DEBUG:
                return f'{settings.LOCAL_BASE_URL}{self.image.url}'
            return f'{settings.PROD_BASE_URL}{self.image.url}'
        else:
            return None

    @property
    def tokens(self):
        refresh = RefreshToken.for_user(self)
        data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }
        return data

    def __str__(self):
        return self.email
