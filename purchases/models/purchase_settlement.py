from django.db import models
from core.models import BaseModel
from .purchase import Purchase
from .purchase_payment_mode import PurchasePaymentMode


class PurchaseSettlement(BaseModel):
    purchase = models.ForeignKey(
        Purchase,
        on_delete=models.CASCADE,
        related_name='settlements',
    )

    amount = models.DecimalField(
        max_digits=14,
        decimal_places=2,
    )

    payment_mode = models.ForeignKey(
        PurchasePaymentMode,
        on_delete=models.PROTECT,
        related_name='settlements',
    )

    reference_number = models.TextField(
        blank=True,
    )

    remarks = models.TextField(
        blank=True,
    )

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return str(self.amount)
