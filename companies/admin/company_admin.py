from django.contrib import admin

from companies.models import Company


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'owner',
        'phone',
        'is_active'
    )

    search_fields = (
        'name',
        'legal_name',
        'phone',
        'email'
    )

    def has_delete_permission(self, request, obj=None):
        return False
