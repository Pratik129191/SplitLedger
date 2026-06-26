from django.db.models import Q
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
                Q(name__icontains=search)
                |
                Q(phone__icontains=search)
                |
                Q(email__icontains=search)
            )

        return queryset.order_by('name')
