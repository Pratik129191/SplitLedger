from django.contrib import admin
from inventory.models import Stock


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = (
        'company_product',
        'quantity',
    )

    search_fields = (
        'company_product__product_master__name',
    )

    def has_delete_permission(self, request, obj=None):
        return False
