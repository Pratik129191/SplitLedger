from django.db import models
from core.models import BaseModel
from products.models import CompanyProduct
from .master_sale import MasterSale


class MasterSaleItem(BaseModel):
    sale = models.ForeignKey(
        MasterSale,
        on_delete=models.CASCADE,
        related_name='items'
    )

    company_product = models.ForeignKey(
        CompanyProduct,
        on_delete=models.PROTECT,
        related_name='sale_items'
    )

    quantity = models.DecimalField(
        max_digits=14,
        decimal_places=3,
    )

    product_name_snapshot = models.CharField(
        max_length=255,
    )

    unit_snapshot = models.CharField(
        max_length=255,
    )

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


