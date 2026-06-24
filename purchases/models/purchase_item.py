from django.db import models
from core.models import BaseModel
from products.models import CompanyProduct
from .purchase import Purchase


class PurchaseItem(BaseModel):
    purchase = models.ForeignKey(
        Purchase,
        on_delete=models.CASCADE,
        related_name='items',
    )

    company_product = models.ForeignKey(
        CompanyProduct,
        on_delete=models.PROTECT,
        related_name='purchase_items',
    )

    quantity = models.DecimalField(
        max_digits=14,
        decimal_places=3,
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




