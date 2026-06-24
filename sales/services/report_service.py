from django.db.models import Sum
from sales.models import MasterSaleItem
from core.constants import SaleStatus


class ReportService:
    @staticmethod
    def top_selling_products(limit=10):
        return MasterSaleItem.objects.filter(
            sale__status=SaleStatus.POSTED
        ).values(
            'product_name_snapshot'
        ).annotate(
            total_qty=Sum('quantity'),
        ).order_by(
            '-total_qty',
        )[:limit]



