from purchases.models import Purchase


class PurchaseNumberService:
    @staticmethod
    def generate_purchase_number(company):
        latest_purchase = Purchase.objects.filter(
            company=company,
        ).order_by('-created_at').first()

        prefix = company.name[:3].upper()
        if latest_purchase is None:
            return f"PUR-{prefix}-0000000001"

        latest_number = int(latest_purchase.invoice_number.split("-")[-1])
        next_number = latest_number + 1
        return f"PUR-{prefix}-{next_number:010d}"



