from django.contrib import admin
from inventory.models import StockMovement


@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = (
        'company_product',
        'movement_type',
        'quantity',
        'created_at',
    )

    list_filter = (
        'movement_type',
    )

    search_fields = (
        'company_product__product_master__name',
    )

