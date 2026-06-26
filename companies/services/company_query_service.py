from django.db.models import Q
from companies.models import Company


class CompanyQueryService:
    @staticmethod
    def search(*, user, search=None):
        queryset = Company.objects.filter(
            owner_id=user.id,
            is_active=True
        )

        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(legal_name__icontains=search) |
                Q(phone__icontains=search)
            )
        return queryset.order_by('name')
