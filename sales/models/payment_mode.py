from django.conf import settings
from django.db import models
from core.models import BaseModel


class SalePaymentMode(BaseModel):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='payment_modes',
    )

    name = models.CharField(
        max_length=200,
    )

    notes = models.TextField(
        blank=True,
    )

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


