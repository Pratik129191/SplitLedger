from vendors.models import Vendor


class VendorQueryService:
    @staticmethod
    def search(*, user, search=None):
        queryset = Vendor.objects.filter(
            owner=user,
            is_active=True
        )

        if search:
            queryset = queryset.filter(
                name__icontains=search
            )
        return queryset.order_by('name')
