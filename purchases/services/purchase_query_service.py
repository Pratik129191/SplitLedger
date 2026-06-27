from django.db.models import Q
from purchases.models import Purchase


class PurchaseQueryService:
    @staticmethod
    def search(*, user, search=None):
        queryset = Purchase.objects.select_related(
            'company', 'vendor'
        ).filter(
            company__owner=user,
        )

        if search:
            queryset = queryset.filter(
                Q(invoice_number__icontains=search)
                |
                Q(vendor__name__icontains=search)
            )
        return queryset.order_by('-created_at')
