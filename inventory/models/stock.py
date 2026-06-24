from django.db import models
from core.models import BaseModel
from products.models import CompanyProduct


class Stock(BaseModel):
    company_product = models.OneToOneField(
        CompanyProduct,
        on_delete=models.CASCADE,
        related_name='stock',
    )

    quantity = models.DecimalField(
        max_digits=14,
        decimal_places=3,
        default=0,
    )

    class Meta:
        ordering = ('company_product__product_master__name',)

    def __str__(self):
        return f"{self.company_product} [{self.quantity} {self.company_product.product_master.unit}]"


