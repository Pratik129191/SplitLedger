from decimal import Decimal
from sales.models import SaleSettlement
from core.exceptions import ValidationException
from core.constants import SaleStatus


class SettlementService:
    @staticmethod
    def create_settlement(*, sale, amount, payment_mode, reference_number="", remarks=""):
        if sale.status == SaleStatus.CANCELLED:
            raise ValidationException(
                'Cannot settle cancelled sale.'
            )

        amount = Decimal(str(amount))
        remaining_amount = (sale.total_amount - sale.returned_amount) - sale.paid_amount

        if amount > remaining_amount:
            raise ValidationException(
                'Settlement exceeds outstanding amount.'
            )
        return SaleSettlement.objects.create(
            sale=sale,
            amount=amount,
            payment_mode=payment_mode,
            reference_number=reference_number,
            remarks=remarks,
        )



