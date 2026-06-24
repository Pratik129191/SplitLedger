from decimal import Decimal
from core.exceptions import ValidationException
from purchases.models import PurchaseSettlement
from core.constants import PurchaseStatus


class PurchaseSettlementService:
    @staticmethod
    def create_settlement(*, purchase, amount, payment_mode, reference_number="", remarks=""):
        if purchase.status == PurchaseStatus.CANCELLED:
            raise ValidationException(
                'Cannot settle cancelled purchase.'
            )

        amount = Decimal(str(amount))
        remaining_amount = purchase.total_amount - purchase.paid_amount

        if amount > remaining_amount:
            raise ValidationException(
                'Settlement exceeds outstanding amount.'
            )
        return PurchaseSettlement.objects.create(
            purchase=purchase,
            amount=amount,
            payment_mode=payment_mode,
            reference_number=reference_number,
            remarks=remarks,
        )

