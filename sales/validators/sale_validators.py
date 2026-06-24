from core.exceptions import ValidationException


def validate_sale_items(items):
    if not items:
        raise ValidationException('Sale must contain at least one item.')


def validate_quantity(quantity):
    if quantity <= 0:
        raise ValidationException('Quantity must be greater than zero.')


def validate_settlement_amount(settlement_amount, total_amount):
    if settlement_amount > total_amount:
        raise ValidationException('Settlement exceeds invoice total.')


