from django.db import models
from core.models import BaseModel
from .master_sale import MasterSale


class SaleReturn(BaseModel):
    sale = models.ForeignKey(
        MasterSale,
        on_delete=models.PROTECT,
        related_name='returns',
    )

    notes = models.TextField(
        blank=True,
    )

    total_amount = models.DecimalField(
        max_digits=14,
        decimal_places=3,
        default=0,
    )

    class Meta:
        ordering = ('-created_at', )

    def __str__(self):
        return f"Return against {self.sale.invoice_number}"



