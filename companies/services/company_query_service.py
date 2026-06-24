from companies.models import Company


class CompanyQueryService:
    @staticmethod
    def search(*, user, search=None):
        queryset = Company.objects.filter(
            owner_id=user.id
        )

        if search:
            queryset = queryset.filter(
                name__icontains=search
            )
        return queryset.order_by('name')
