from purchases.models import Purchase


class PurchaseSearchService:
    @staticmethod
    def search(*, invoice_number=None, vendor=None, from_date=None, to_date=None):
        queryset = Purchase.objects.all()

        if invoice_number:
            queryset = queryset.filter(
                invoice_number__icontains=invoice_number
            )

        if vendor:
            queryset = queryset.filter(
                vendor=vendor
            )

        if from_date:
            queryset = queryset.filter(
                created_at__date__gte=from_date
            )

        if to_date:
            queryset = queryset.filter(
                created_at__date__lte=to_date
            )

        return queryset.order_by('-created_at')


