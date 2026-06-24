from decimal import Decimal
from django.db import transaction
from core.constants import PurchaseStatus
from core.exceptions import ValidationException
from licensing.services import LicenseService
from purchases.models import Purchase, PurchaseItem
from inventory.services import StockService
from purchases.validators import validate_purchase_items, validate_purchase_quantity
from .purchase_number_service import PurchaseNumberService


class PurchaseService:
    @staticmethod
    @transaction.atomic
    def create_purchase(*, company, vendor, notes="", items=None):
        LicenseService().assert_can_create_purchase()
        validate_purchase_items(items)
        purchase = Purchase.objects.create(
            company=company,
            vendor=vendor,
            invoice_number=PurchaseNumberService.generate_purchase_number(company),
            notes=notes,
        )

        subtotal = Decimal('0')

        for item in items:
            company_product = item['company_product']
            quantity = Decimal(str(item['quantity']))
            rate = Decimal(str(item['rate']))

            validate_purchase_quantity(quantity)
            amount = quantity * rate

            PurchaseItem.objects.create(
                purchase=purchase,
                company_product=company_product,
                quantity=quantity,
                rate_snapshot=rate,
                amount_snapshot=amount,
            )
            StockService.add_stock(
                company_product=company_product,
                quantity=quantity,
                remarks=purchase.invoice_number,
            )
            subtotal += amount

        purchase.subtotal_amount = subtotal
        purchase.total_amount = subtotal

        purchase.save()
        return purchase


    @staticmethod
    @transaction.atomic
    def update_purchase(*, purchase, vendor, notes="", items=None):
        if purchase.status == PurchaseStatus.CANCELLED:
            raise ValidationException(
                'Cancelled purchase cannot be edited.'
            )

        validate_purchase_items(items)

        paid_amount = purchase.paid_amount
        new_total = Decimal('0')
        for item in items:
            quantity = Decimal(str(item['quantity']))
            rate = Decimal(str(item['rate']))
            new_total += quantity * rate

        if new_total < paid_amount:
            raise ValidationException(
                'Purchase total cannot be reduced below paid amount.'
            )

        for old_item in purchase.items.select_related('company_product'):
            StockService.restore_purchase_stock(
                company_product=old_item.company_product,
                quantity=old_item.quantity,
                remarks=f"Edit restore {purchase.invoice_number}",
            )

        purchase.items.all().delete()
        subtotal = Decimal('0')

        for item in items:
            company_product = item['company_product']
            quantity = Decimal(str(item['quantity']))
            rate = Decimal(str(item['rate']))

            validate_purchase_quantity(quantity)
            amount = quantity * rate

            PurchaseItem.objects.create(
                purchase=purchase,
                company_product=company_product,
                quantity=quantity,
                rate_snapshot=rate,
                amount_snapshot=amount,
            )

            StockService.add_stock(
                company_product=company_product,
                quantity=quantity,
                remarks=f"Edit add {purchase.invoice_number}"
            )
            subtotal += amount

        purchase.vendor = vendor
        purchase.notes = notes
        purchase.subtotal_amount = subtotal
        purchase.total_amount = subtotal
        purchase.save()
        return purchase


    @staticmethod
    @transaction.atomic
    def cancel_purchase(*, purchase):
        if purchase.status == PurchaseStatus.CANCELLED:
            raise ValidationException(
                'Purchase already cancelled.'
            )

        if purchase.paid_amount > 0:
            raise ValidationException(
                'Cannot cancel a settled purchase.'
            )

        for item in purchase.items.select_related('company_product'):
            StockService.restore_purchase_stock(
                company_product=item.company_product,
                quantity=item.quantity,
                remarks=f"Cancelled {purchase.invoice_number}",
            )

        purchase.status = PurchaseStatus.CANCELLED
        purchase.save()
        return purchase


