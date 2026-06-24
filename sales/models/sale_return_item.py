from django.db import models
from core.models import BaseModel
from .sale_return import SaleReturn
from .master_sale_item import MasterSaleItem


class SaleReturnItem(BaseModel):
    sale_return = models.ForeignKey(
        SaleReturn,
        on_delete=models.CASCADE,
        related_name='items'
    )

    master_sale_item = models.ForeignKey(
        MasterSaleItem,
        on_delete=models.CASCADE,
        related_name='returned_items'
    )

    quantity = models.DecimalField(
        max_digits=14,
        decimal_places=3,
    )

    amount_snapshot = models.DecimalField(
        max_digits=14,
        decimal_places=2,
    )

    class Meta:
        ordering = ('-created_at',)


