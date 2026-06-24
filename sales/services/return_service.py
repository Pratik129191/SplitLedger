from decimal import Decimal
from django.db import transaction
from django.db.models import Sum
from inventory.services import StockService
from sales.models import SaleReturn, SaleReturnItem
from core.exceptions import ValidationException
from core.constants import SaleStatus


class ReturnService:
    @staticmethod
    @transaction.atomic
    def create_return(*, sale, items, notes=""):
        if sale.status == SaleStatus.CANCELLED:
            raise ValidationException(
                "Cannot return cancelled sale."
            )

        sale_return = SaleReturn.objects.create(
            sale=sale,
            notes=notes,
        )
        total_amount = Decimal('0')

        for item in items:
            sale_item = item['sale_item']
            quantity = Decimal(str(item['quantity']))

            already_returned = sale_item.returned_items.aggregate(
                total=Sum('quantity')
            )['total'] or 0
            if already_returned + quantity > sale_item.quantity:
                raise ValidationException(
                    f'Cannot return more than sold quantity for {sale_item.product_name_snapshot}'
                )

            unit_rate = (sale_item.amount_snapshot / sale_item.quantity)
            amount = quantity * unit_rate

            SaleReturnItem.objects.create(
                sale_return=sale_return,
                master_sale_item=sale_item,
                quantity=quantity,
                amount_snapshot=amount,
            )

            StockService.add_stock(
                company_product=sale_item.company_product,
                quantity=quantity,
                remarks=f"Return against {sale.invoice_number}",
            )
            total_amount += amount

        sale_return.total_amount = total_amount
        sale_return.save()
        return sale_return

