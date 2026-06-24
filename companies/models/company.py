from django.conf import settings
from django.db import models
from core.models import BaseModel


class Company(BaseModel):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='companies',
    )

    name = models.CharField(max_length=150)

    legal_name = models.CharField(
        max_length=255,
        blank=True,
    )

    phone = models.CharField(
        max_length=20,
        blank=True,
    )

    email = models.EmailField(
        blank=True,
    )

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


