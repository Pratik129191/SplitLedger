from django.db.models import Q
from inventory.models import Stock, StockMovement


class StockQueryService:
    @staticmethod
    def stock_search(*, user, search=None):
        stocks = Stock.objects.select_related(
            'company_product',
            'company_product__company',
            'company_product__product_master',
        ).filter(
            company_product__company_owner=user,
        ).order_by(
            'company_product__product_master__name',
        )

        if search:
            stocks = stocks.filter(
                Q(company_product__product_master__name__icontains=search)
            )
        return stocks

    @staticmethod
    def stock_movement_search(*, user, search=None):
        stock_movement = StockMovement.objects.select_related(
            "company_product",
            "company_product__company",
            "company_product__product_master",
        ).filter(
            company_product__company__owner=user
        )

        if search:
            stock_movement = stock_movement.filter(
                Q(company_product__product_master__name__icontains=search)
            )
        return stock_movement
