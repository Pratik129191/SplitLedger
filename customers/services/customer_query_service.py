from customers.models import Customer


class CustomerQueryService:

    @staticmethod
    def search(*, user, search=None):
        queryset = Customer.objects.filter(
            owner=user,
            is_active=True
        )

        if search:
            queryset = queryset.filter(
                name__icontains=search
            )

        return queryset.order_by('name')
