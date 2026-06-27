from django.contrib import admin
from inventory.models import Stock


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = (
        'company_product',
        'quantity',
    )

    list_filter = (
        "company_product__company",
    )

    search_fields = (
        'company_product__product_master__name',
    )

    ordering = (
        "company_product__product_master__name",
    )

    def has_delete_permission(self, request, obj=None):
        return False
