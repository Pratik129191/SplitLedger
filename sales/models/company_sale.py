from django.db import models
from core.models import BaseModel
from core.constants import SaleStatus
from companies.models import Company
from .master_sale import MasterSale


class CompanySale(BaseModel):
    company = models.ForeignKey(
        Company,
        on_delete=models.PROTECT,
        related_name='company_sales'
    )

    master_sale = models.ForeignKey(
        MasterSale,
        on_delete=models.PROTECT,
        related_name='company_sales'
    )

    invoice_number = models.CharField(
        max_length=50,
        unique=True,
    )

    status = models.CharField(
        max_length=SaleStatus.MAX_LENGTH,
        choices=SaleStatus.CHOICES,
        default=SaleStatus.POSTED,
    )

    source_master_invoice_number = models.CharField(
        max_length=50,
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
    def source_master_sale(self):
        return self.master_sale

    @property
    def item_count(self):
        return self.items.count()
    
    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.invoice_number



