from django.conf import settings
from django.db import models
from django.db.models import Sum
from core.models import BaseModel
from core.constants import PurchaseStatus


class Vendor(BaseModel):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='vendors',
    )

    name = models.CharField(
        max_length=255,
    )

    phone = models.CharField(
        max_length=20,
        blank=True,
    )

    email = models.EmailField(
        blank=True,
    )

    address = models.TextField(
        blank=True,
    )

    notes = models.TextField(
        blank=True,
    )

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

    @property
    def total_purchase_amount(self):
        return self.purchases.filter(
            status=PurchaseStatus.POSTED,
        ).aggregate(
            total=Sum('total_amount')
        )['total'] or 0

    @property
    def total_paid_amount(self):
        return self.purchases.aggregate(
            total=Sum('settlements__amount')
        )['total'] or 0

    @property
    def outstanding_amount(self):
        return self.total_purchase_amount - self.total_paid_amount
