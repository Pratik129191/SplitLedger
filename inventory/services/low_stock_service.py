from inventory.models import Stock


class LowStockService:
    @staticmethod
    def get_low_stock_products(threshold=10):
        return Stock.objects.select_related(
            'company_product',
            'company_product__product_master',
        ).filter(
            quantity__lte=threshold,
        ).order_by(
            'quantity',
        )
