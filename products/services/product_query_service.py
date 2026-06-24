from products.models import CompanyProduct


class ProductQueryService:

    @staticmethod
    def search(*, user, search=None):
        queryset = CompanyProduct.objects.select_related(
            "company",
            "product_master"
        ).filter(
            company__owner=user,
            is_active=True
        )

        if search:
            queryset = queryset.filter(
                product_master__name__icontains=search
            )

        return queryset.order_by(
            "product_master__name"
        )
