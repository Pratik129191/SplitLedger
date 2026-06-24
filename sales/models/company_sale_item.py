from django.db import models
from core.models import BaseModel
from .company_sale import CompanySale
from .master_sale_item import MasterSaleItem


class CompanySaleItem(BaseModel):
    company_sale = models.ForeignKey(
        CompanySale,
        on_delete=models.CASCADE,
        related_name='items'
    )

    master_sale_item = models.ForeignKey(
        MasterSaleItem,
        on_delete=models.PROTECT,
        related_name='company_sale_items'
    )

    quantity = models.DecimalField(
        max_digits=14,
        decimal_places=3,
    )

    product_name_snapshot = models.CharField(max_length=255)
    unit_snapshot = models.CharField(max_length=50)
    rate_snapshot = models.DecimalField(
        max_digits=14,
        decimal_places=2,
    )
    amount_snapshot = models.DecimalField(
        max_digits=14,
        decimal_places=2,
    )

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.product_name_snapshot
