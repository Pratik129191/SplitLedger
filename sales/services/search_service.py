from sales.models import MasterSale


class SaleSearchService:
    @staticmethod
    def search(*, user, invoice_number=None, customer=None, from_date=None, to_date=None):
        queryset = MasterSale.objects.select_related(
            'customer'
        ).filter(
            owner=user
        )

        if invoice_number:
            queryset = queryset.filter(
                invoice_number__icontains=invoice_number
            )

        if customer:
            queryset = queryset.filter(
                customer=customer
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
