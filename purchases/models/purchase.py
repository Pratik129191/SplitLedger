from django.db import models
from django.db.models import Sum
from core.models import BaseModel
from core.constants import PurchaseStatus
from companies.models import Company
from vendors.models import Vendor


class Purchase(BaseModel):
    company = models.ForeignKey(
        Company,
        on_delete=models.PROTECT,
        related_name='purchases',
    )

    vendor = models.ForeignKey(
        Vendor,
        on_delete=models.PROTECT,
        related_name='purchases',
    )

    invoice_number = models.CharField(
        max_length=50,
        unique=True,
    )

    status = models.CharField(
        max_length=PurchaseStatus.MAX_LENGTH,
        choices=PurchaseStatus.CHOICES,
        default=PurchaseStatus.POSTED
    )

    notes = models.TextField(
        blank=True,
    )

    subtotal_amount = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=0,
    )

    total_amount = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=0,
    )

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.invoice_number
    
    @property
    def paid_amount(self):
        return self.settlements.aggregate(
            total=Sum('amount')
        )['total'] or 0

    @property
    def outstanding_amount(self):
        return self.total_amount - self.paid_amount
    
