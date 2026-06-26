from django.conf import settings
from django.db import models
from django.db.models import Sum
from core.models import BaseModel
from core.constants import SaleStatus


class Customer(BaseModel):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='customers',
    )

    name = models.CharField(
        max_length=250,
        db_index=True,
    )

    phone = models.CharField(
        max_length=20,
        blank=True,
        db_index=True,
    )

    email = models.EmailField(
        blank=True,
        db_index=True,
    )

    address = models.TextField(
        blank=True,
    )

    notes = models.TextField(
        blank=True,
    )

    class Meta:
        ordering = ('name',)
        constraints = [
            models.UniqueConstraint(
                fields=["owner", "name"],
                name="unique_customer_per_owner"
            )
        ]

    def __str__(self):
        return self.name

    @property
    def total_sales_amount(self):
        return self.sales.filter(
            status=SaleStatus.POSTED
        ).aggregate(
            total=Sum('total_amount')
        )['total'] or 0

    @property
    def total_return_amount(self):
        return self.sales.filter(
            status=SaleStatus.POSTED
        ).aggregate(
            total=Sum('returns__total_amount')
        )['total'] or 0

    @property
    def total_received_amount(self):
        return self.sales.filter(
            status=SaleStatus.POSTED
        ).aggregate(
            total=Sum('settlements__amount')
        )['total'] or 0

    @property
    def outstanding_amount(self):
        return (self.total_sales_amount - self.total_return_amount) - self.total_received_amount
