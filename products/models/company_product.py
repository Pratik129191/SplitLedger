from django.db import models
from core.models import BaseModel
from companies.models import Company
from .product_master import ProductMaster


class CompanyProduct(BaseModel):
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name='company_products',
    )

    product_master = models.ForeignKey(
        ProductMaster,
        on_delete=models.CASCADE,
        related_name='company_products',
    )

    selling_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
    )

    class Meta:
        ordering = ('product_master__name',)
        constraints = [
            models.UniqueConstraint(
                fields=['company', 'product_master'],
                name='unique_company_product_mapping'
            )
        ]

    def __str__(self):
        return f"{self.product_master.name} - {self.company.name}"
