from django.contrib import admin

from products.models import ProductMaster


@admin.register(ProductMaster)
class ProductMasterAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'unit',
        'is_active'
    )

    list_filter = (
        'unit',
        'is_active',
    )

    ordering = (
        'name',
    )

    search_fields = (
        'name',
    )

    def has_delete_permission(self, request, obj=None):
        return False
