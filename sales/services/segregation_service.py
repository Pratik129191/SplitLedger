from collections import defaultdict
from sales.models import (
    CompanySale,
    CompanySaleItem,
)
from sales.services import InvoiceNumberService


class SegregationService:
    @staticmethod
    def generate_company_sales(master_sale):
        if master_sale.company_sales.exists():
            return list(master_sale.company_sales.all())

        grouped_items = defaultdict(list)
        for item in master_sale.items.select_related('company_product__company'):
            company = item.company_product.company
            grouped_items[company].append(item)

        generated_sales = []
        for company, items in grouped_items.items():
            company_sale = CompanySale.objects.create(
                company=company,
                master_sale=master_sale,
                invoice_number=InvoiceNumberService.generate_company_sale_number(company),
                source_master_invoice_number=master_sale.invoice_number,
            )

            total = 0
            for item in items:
                CompanySaleItem.objects.create(
                    company_sale=company_sale,
                    master_sale_item=item,
                    product_name_snapshot=item.product_name_snapshot,
                    unit_snapshot=item.unit_snapshot,
                    rate_snapshot=item.rate_snapshot,
                    amount_snapshot=item.amount_snapshot,
                    quantity=item.quantity,
                )
                total += item.amount_snapshot

            company_sale.subtotal_amount = total
            company_sale.total_amount = total
            company_sale.save()

            generated_sales.append(company_sale)
        return generated_sales

    @staticmethod
    def rebuild_company_sales(master_sale):
        master_sale.company_sales.all().delete()
        return SegregationService.generate_company_sales(
            master_sale
        )



