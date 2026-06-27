from core.exceptions import ValidationException


def validate_stock_availability(available_quantity, requested_quantity):
    if requested_quantity <= 0:
        raise ValidationException(
            "Quantity must be greater than zero."
        )

    if requested_quantity > available_quantity:
        raise ValidationException('Insufficient stock.')
