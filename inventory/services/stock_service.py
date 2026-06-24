from decimal import Decimal
from inventory.models import Stock, StockMovement
from core.constants import StockMovementTypes
from inventory.validators import validate_stock_availability


class StockService:
    @staticmethod
    def get_or_create_stock(company_product):
        stock, _ = Stock.objects.get_or_create(
            company_product=company_product,
        )
        return stock

    @staticmethod
    def add_stock(*, company_product, quantity, remarks=""):
        stock = StockService.get_or_create_stock(company_product)
        stock.quantity += Decimal(str(quantity))
        stock.save()

        StockMovement.objects.create(
            company_product=company_product,
            movement_type=StockMovementTypes.PURCHASE,
            quantity=quantity,
            remarks=remarks,
        )

    @staticmethod
    def consume_stock(*, company_product, quantity, remarks=""):
        stock = StockService.get_or_create_stock(company_product)
        validate_stock_availability(stock.quantity, quantity)
        stock.quantity -= Decimal(str(quantity))
        stock.save()

        StockMovement.objects.create(
            company_product=company_product,
            movement_type=StockMovementTypes.SALE,
            quantity=quantity,
            remarks=remarks,
        )

    @staticmethod
    def restore_sale_stock(*, company_product, quantity, remarks=""):
        StockService.add_stock(
            company_product=company_product,
            quantity=quantity,
            remarks=remarks,
        )

    @staticmethod
    def restore_purchase_stock(*, company_product, quantity, remarks=""):
        StockService.consume_stock(
            company_product=company_product,
            quantity=quantity,
            remarks=remarks,
        )



