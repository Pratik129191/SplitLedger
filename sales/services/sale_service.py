from decimal import Decimal
from django.db import transaction
from licensing.services import LicenseService
from core.constants import SaleStatus
from core.exceptions import ValidationException
from sales.models import (
    MasterSale,
    MasterSaleItem
)
from sales.validators import (
    validate_settlement_amount,
    validate_sale_items,
    validate_quantity,
)
from sales.services import (
    InvoiceNumberService,
    SettlementService,
    SegregationService,
)
from inventory.services import StockService


class SaleService:
    @staticmethod
    @transaction.atomic
    def create_sale(*, owner, customer=None, notes="", items, initial_settlement=None):
        LicenseService().assert_can_create_sale()
        validate_sale_items(items)

        invoice_number = InvoiceNumberService.generate_master_sale_number()
        sale = MasterSale.objects.create(
            invoice_number=invoice_number,
            owner=owner,
            customer=customer,
            notes=notes,
        )
        
        subtotal = Decimal('0')
        for item in items:
            company_product = item['company_product']
            quantity = Decimal(str(item['quantity']))
            validate_quantity(quantity)
            rate = company_product.selling_price
            amount = quantity * rate

            MasterSaleItem.objects.create(
                sale=sale,
                company_product=company_product,
                quantity=quantity,

                product_name_snapshot=company_product.product_master.name,
                unit_snapshot=company_product.product_master.unit,
                rate_snapshot=rate,
                amount_snapshot=amount,
            )
            StockService.consume_stock(
                company_product=company_product,
                quantity=quantity,
                remarks=sale.invoice_number,
            )
            subtotal += amount

        sale.subtotal_amount = subtotal
        sale.total_amount = subtotal
        sale.save()

        if initial_settlement:
            amount = Decimal(str(initial_settlement['amount']))
            validate_settlement_amount(amount, sale.total_amount)
            SettlementService.create_settlement(
                sale=sale,
                amount=amount,
                payment_mode=initial_settlement['payment_mode'],
                reference_number=initial_settlement.get('reference_number', ""),
                remarks=initial_settlement.get('remarks', ""),
            )

        SegregationService.generate_company_sales(sale)
        return sale


    @staticmethod
    @transaction.atomic
    def update_sale(*, sale, customer=None, notes="", items):
        if sale.status == SaleStatus.CANCELLED:
            raise ValidationException(
                'Cancelled sale cannot be edited.'
            )

        validate_sale_items(items)

        # protection for invalid sale invoice modification
        paid_amount = sale.paid_amount
        returned_amount = sale.returned_amount
        new_total = Decimal('0')

        for item in items:
            company_product = item['company_product']
            quantity = Decimal(str(item['quantity']))
            validate_quantity(quantity)

            rate = company_product.selling_price
            amount = quantity * rate
            new_total += amount

        if new_total < (paid_amount + returned_amount):
            raise ValidationException(
                'Invoice total cannot be reduced below settled and returned amount.'
            )

        for old_item in sale.items.select_related('company_product'):
            StockService.restore_sale_stock(
                company_product=old_item.company_product,
                quantity=old_item.quantity,
                remarks=f"Edit restore {sale.invoice_number}"
            )

        sale.company_sales.all().delete()
        sale.items.all().delete()
        subtotal = Decimal('0')

        for item in items:
            company_product = item['company_product']
            quantity = Decimal(str(item['quantity']))
            validate_quantity(quantity)
            rate = company_product.selling_price
            amount = quantity * rate
            MasterSaleItem.objects.create(
                sale=sale,
                company_product=company_product,
                quantity=quantity,
                product_name_snapshot=company_product.product_master.name,
                unit_snapshot=company_product.product_master.unit,
                rate_snapshot=rate,
                amount_snapshot=amount,
            )

            StockService.consume_stock(
                company_product=company_product,
                quantity=quantity,
                remarks=f"Edit consume {sale.invoice_number}"
            )
            subtotal += amount

        sale.customer = customer
        sale.notes = notes
        sale.subtotal_amount = subtotal
        sale.total_amount = subtotal
        sale.save()

        SegregationService.generate_company_sales(
            sale
        )
        return sale


    @staticmethod
    @transaction.atomic
    def cancel_sale(*, sale):
        if sale.paid_amount > 0:
            raise ValidationException(
                'Cannot cancel a settled sale.'
            )

        if sale.returned_amount > 0:
            raise ValidationException(
                'Cannot cancel a returned sale.'
            )

        if sale.status == SaleStatus.CANCELLED:
            raise ValidationException(
                'Sale already cancelled.'
            )

        for item in sale.items.select_related('company_product'):
            StockService.restore_sale_stock(
                company_product=item.company_product,
                quantity=item.quantity,
                remarks=f"Cancelled {sale.invoice_number}"
            )

        sale.status = SaleStatus.CANCELLED
        sale.save()
        sale.company_sales.update(
            status=SaleStatus.CANCELLED
        )
        return sale




