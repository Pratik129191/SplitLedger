from django.contrib import admin
from customers.models import Customer


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'phone',
        'total_sales_amount',
        'total_received_amount',
        'outstanding_amount',
    )

    search_fields = (
        'name',
        'phone',
    )

    def has_delete_permission(self, request, obj=None):
        return False
