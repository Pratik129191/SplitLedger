from django.db import models
from django.db.models import Sum
from django.conf import settings
from core.models import BaseModel
from customers.models import Customer
from core.constants import SaleStatus


class MasterSale(BaseModel):
    invoice_number = models.CharField(
        max_length=50,
        unique=True,
    )

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='master_sales',
    )

    customer = models.ForeignKey(
        Customer,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='sales',
    )

    status = models.CharField(
        max_length=SaleStatus.MAX_LENGTH,
        choices=SaleStatus.CHOICES,
        default=SaleStatus.POSTED,
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

    @property
    def paid_amount(self):
        return self.settlements.aggregate(
            total=Sum('amount')
        )['total'] or 0

    @property
    def returned_amount(self):
        return self.returns.aggregate(
            total=Sum('total_amount')
        )['total'] or 0

    @property
    def outstanding_amount(self):
        return (self.total_amount - self.returned_amount) - self.paid_amount

    @property
    def generated_company_sales(self):
        return self.company_sales.all()

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.invoice_number




