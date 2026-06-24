from core.exceptions import ValidationException


def validate_purchase_items(items):
    if not items:
        raise ValidationException("Purchase must contain at least one item")


def validate_purchase_quantity(quantity):
    if quantity <= 0:
        raise ValidationException("Quantity must be greater than zero.")



