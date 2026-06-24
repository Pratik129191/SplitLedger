from django.contrib import admin
from vendors.models import Vendor


@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'phone',
        'total_purchase_amount',
        'total_paid_amount',
        'outstanding_amount',
    )

    search_fields = (
        'name',
        'phone'
    )

    def has_delete_permission(self, request, obj=None):
        return False
