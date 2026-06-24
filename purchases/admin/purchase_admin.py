from django.contrib import admin
from purchases.models import Purchase, PurchaseItem, PurchaseSettlement, PurchasePaymentMode


class PurchaseItemInline(admin.TabularInline):
    model = PurchaseItem
    extra = 0


class PurchaseSettlementInline(admin.TabularInline):
    model = PurchaseSettlement
    extra = 0


@admin.register(PurchasePaymentMode)
class PurchasePaymentModeAdmin(admin.ModelAdmin):
    list_display = (
        'owner',
        'name',
        'notes'
    )


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = (
        'invoice_number',
        'vendor',
        'total_amount',
        'paid_amount',
        'outstanding_amount',
        'status',
    )

    search_fields = (
        'invoice_number',
        'vendor__name'
    )

    list_filter = (
        'status',
        'created_at',
    )

    autocomplete_fields = (
        'vendor',
    )

    readonly_fields = (
        'subtotal_amount',
        'total_amount',
        'paid_amount',
        'outstanding_amount',
    )

    inlines = (
        PurchaseItemInline,
        PurchaseSettlementInline,
    )

    def has_delete_permission(self, request, obj=None):
        return False
