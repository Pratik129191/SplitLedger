from django.contrib import admin
from sales.models import (
    MasterSale,
    MasterSaleItem,
    SaleSettlement,
    SaleReturn,
)

class MasterSaleItemInline(admin.TabularInline):
    model = MasterSaleItem
    extra = 0
    readonly_fields = (
        'product_name_snapshot',
        'quantity',
        'rate_snapshot',
        'amount_snapshot',
    )


class SaleSettlementInline(admin.TabularInline):
    model = SaleSettlement
    extra = 0


class SaleReturnInline(admin.TabularInline):
    model = SaleReturn
    extra = 0


@admin.register(MasterSale)
class MasterSaleAdmin(admin.ModelAdmin):
        list_display = (
            'invoice_number',
            'customer',
            'total_amount',
            'paid_amount',
            'returned_amount',
            'outstanding_amount',
            'status',
        )

        list_filter = (
            'status',
            'created_at',
        )

        search_fields = (
            'invoice_number',
            'customer__name',
        )

        autocomplete_fields = (
            'customer',
        )

        readonly_fields = (
            'subtotal_amount',
            'total_amount',
            'paid_amount',
            'returned_amount',
            'outstanding_amount',
        )

        inlines = (
            MasterSaleItemInline,
            SaleSettlementInline,
            SaleReturnInline,
        )

        def has_delete_permission(self, request, obj=None):
            return False