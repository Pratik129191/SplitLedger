from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from core.services import DashboardService
from inventory.services import LowStockService


@login_required
def dashboard_view(request):
    context = {
        "today_sales": DashboardService.get_today_sales_amount(),
        "today_purchase": DashboardService.get_today_purchase_amount(),
        "receivable": DashboardService.get_total_receivable(),
        "payable": DashboardService.get_total_payable(),
        "customer_count": DashboardService.get_total_customers(),
        "vendor_count": DashboardService.get_total_vendors(),
        "product_count": DashboardService.get_total_products_in_stock(),
        "low_stock_products": LowStockService.get_low_stock_products(),
        "recent_sales": DashboardService.get_recent_sales(),
        "recent_purchases": DashboardService.get_recent_purchases(),
    }

    return render(
        request,
        "dashboard/dashboard.html",
        context
    )
