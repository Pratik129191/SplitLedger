from django.contrib import admin
from sales.models import CompanySale, CompanySaleItem


class CompanySaleItemInline(admin.TabularInline):
    model = CompanySaleItem
    extra = 0
    readonly_fields = (
        'product_name_snapshot',
        'quantity',
        'rate_snapshot',
        'amount_snapshot',
    )


@admin.register(CompanySale)
class CompanySaleAdmin(admin.ModelAdmin):
    list_display = (
        'invoice_number',
        'company',
        'source_master_invoice_number',
        'total_amount',
        'status',
    )

    list_filter = (
        'company',
        'status',
    )

    search_fields = (
        'invoice_number',
        'company__name',
    )

    readonly_fields = (
        'subtotal_amount',
        'total_amount',
    )

    inlines = (
        CompanySaleItemInline,
    )

    def has_delete_permission(self, request, obj=None):
        return False
