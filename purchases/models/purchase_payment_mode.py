from django.conf import settings
from django.db import models
from core.models import BaseModel


class PurchasePaymentMode(BaseModel):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='purchase_payment_modes',
    )

    name = models.CharField(
        max_length=200,
    )

    notes = models.TextField(
        blank=True,
    )

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.name
    
