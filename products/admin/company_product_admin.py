from django.contrib import admin
from products.models import CompanyProduct


@admin.register(CompanyProduct)
class CompanyProductAdmin(admin.ModelAdmin):
    list_display = (
        'product_master',
        'company',
        'selling_price',
        'is_active'
    )

    search_fields = (
        'product_master__name',
        'company__name',
    )

    list_filter = (
        'company',
        'is_active',
    )

    autocomplete_fields = (
        'company',
        'product_master'
    )

    def has_delete_permission(self, request, obj=None):
        return False
