from sales.models import MasterSale, SaleSettlement, SaleReturn
from core.constants import SaleStatus


class CustomerLedgerService:
    @staticmethod
    def get_customer_ledger(customer):
        entries = []

        sales = MasterSale.objects.filter(
            customer=customer,
            status=SaleStatus.POSTED,
        ).order_by(
            '-created_at'
        )

        for sale in sales:
            entries.append({
                'date': sale.created_at,
                'type': 'SALE',
                'reference': sale.invoice_number,
                'amount': sale.total_amount,
            })

            for settlement in sale.settlements.all():
                entries.append({
                    'date': settlement.created_at,
                    'type': 'RECEIVED',
                    'reference': sale.invoice_number,
                    'amount': settlement.amount,
                })

            for sale_return in sale.returns.all():
                entries.append({
                    'date': sale_return.created_at,
                    'type': 'RETURN',
                    'reference': sale.invoice_number,
                    'amount': sale_return.total_amount
                })

        return sorted(
            entries,
            key=lambda entry: entry['date'],
        )

