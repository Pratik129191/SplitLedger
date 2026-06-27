from django.db import models
from core.models import BaseModel
from core.constants import StockMovementTypes
from products.models import CompanyProduct


class StockMovement(BaseModel):
    company_product = models.ForeignKey(
        CompanyProduct,
        on_delete=models.PROTECT,
        related_name='stock_movements',
    )

    movement_type = models.CharField(
        max_length=StockMovementTypes.MAX_LENGTH,
        choices=StockMovementTypes.CHOICES,
        db_index=True,
    )

    quantity = models.DecimalField(
        max_digits=14,
        decimal_places=3,
    )

    remarks = models.TextField(
        blank=True,
    )

    class Meta:
        ordering = ('-created_at',)
