from django.db import models
from django.contrib.auth.models import AbstractUser
from accounts.managers import CustomUserManager


class User(AbstractUser):
    email = models.EmailField(
        unique=True,
    )

    phone = models.CharField(
        max_length=20,
        blank=True,
    )

    full_name = models.CharField(
        max_length=255,
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']
    objects = CustomUserManager()

    def __str__(self):
        return self.email
