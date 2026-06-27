from inventory.models import Stock


class LowStockService:
    @staticmethod
    def get_low_stock_products(*, user, threshold=10):
        return Stock.objects.select_related(
            'company_product',
            'company_product__product_master',
        ).filter(
            company_product__company__owner=user,
            quantity__lte=threshold,
        ).order_by(
            'quantity',
        )
