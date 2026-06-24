from django.db.models import Sum
from django.utils import timezone

from core.constants import SaleStatus, PurchaseStatus
from customers.models import Customer
from inventory.models import Stock
from purchases.models import Purchase
from sales.models import MasterSale
from vendors.models import Vendor


class DashboardService:
    @staticmethod
    def get_today_sales_amount():
        today = timezone.now().date()
        return MasterSale.objects.filter(
            status=SaleStatus.POSTED,
            created_at__date=today
        ).aggregate(
            total=Sum('total_amount')
        )['total'] or 0

    @staticmethod
    def get_today_purchase_amount():
        today = timezone.now().date()
        return Purchase.objects.filter(
            status=PurchaseStatus.POSTED,
            created_at__date=today
        ).aggregate(
            total=Sum('total_amount')
        )['total'] or 0

    @staticmethod
    def get_total_receivable():
        total = 0
        for customer in Customer.objects.all():
            total += customer.outstanding_amount
        return total

    @staticmethod
    def get_total_payable():
        total = 0
        for vendor in Vendor.objects.all():
            total += vendor.outstanding_amount
        return total

    @staticmethod
    def get_total_customers():
        return Customer.objects.count()

    @staticmethod
    def get_total_vendors():
        return Vendor.objects.count()

    @staticmethod
    def get_total_products_in_stock():
        return Stock.objects.count()

    @staticmethod
    def get_recent_sales(threshold=10):
        return MasterSale.objects.select_related(
            'customer',
        ).order_by(
            '-created_at',
        )[:threshold]

    @staticmethod
    def get_recent_purchases(threshold=10):
        return Purchase.objects.select_related(
            'vendor',
        ).order_by(
            '-created_at',
        )[:threshold]
