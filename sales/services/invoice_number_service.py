from sales.models import MasterSale, CompanySale


class InvoiceNumberService:
    @staticmethod
    def generate_master_sale_number():
        latest_sale = MasterSale.objects.order_by(
            '-created_at'
        ).first()

        if latest_sale is None:
            return "INV-0000000001"

        last_number = int(latest_sale.invoice_number.split("-")[-1])
        next_number = last_number + 1
        return f"INV-{next_number:010d}"


    @staticmethod
    def generate_company_sale_number(company):
        latest_company_sale = CompanySale.objects.filter(
            company=company,
        ).order_by(
            '-created_at'
        ).first()

        prefix = company.name[:3].upper()
        if latest_company_sale is None:
            return f"{prefix}-0000000001"

        last_number = int(latest_company_sale.invoice_number.split("-")[-1])
        next_number = last_number + 1
        return f"{prefix}-{next_number:010d}"

