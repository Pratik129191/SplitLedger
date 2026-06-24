from django.db import models
from core.models import BaseModel
from .master_sale import MasterSale
from .payment_mode import SalePaymentMode


class SaleSettlement(BaseModel):
    sale = models.ForeignKey(
        MasterSale,
        on_delete=models.CASCADE,
        related_name='settlements',
    )

    amount = models.DecimalField(
        max_digits=14,
        decimal_places=2,
    )

    payment_mode = models.ForeignKey(
        SalePaymentMode,
        on_delete=models.PROTECT,
        related_name='settlements',
    )

    reference_number = models.CharField(
        max_length=100,
        blank=True,
    )

    remarks = models.TextField(
        blank=True,
    )

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return str(self.amount)
