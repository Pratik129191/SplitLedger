from purchases.models import Purchase, PurchaseSettlement
from core.constants import PurchaseStatus


class VendorLedgerService:
    @staticmethod
    def get_vendor_ledger(vendor):
        entries = []

        purchases = Purchase.objects.filter(
            vendor=vendor,
            status=PurchaseStatus.POSTED
        ).order_by(
            '-created_at'
        )

        for purchase in purchases:
            entries.append({
                'date': purchase.created_at,
                'type': 'PURCHASE',
                'reference': purchase.invoice_number,
                'amount': purchase.total_amount,
            })

            for settlement in purchase.settlements.all():
                entries.append({
                    'date': settlement.created_at,
                    'type': 'PAID',
                    'reference': purchase.invoice_number,
                    'amount': settlement.amount,
                })

        return sorted(
            entries,
            key=lambda entry: entry['date'],
            reverse=True
        )
