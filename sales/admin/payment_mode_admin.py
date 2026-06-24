from django.contrib import admin
from sales.models import SalePaymentMode


@admin.register(SalePaymentMode)
class PaymentModeAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'owner',
        'is_active',
    )



