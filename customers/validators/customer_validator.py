from core.exceptions import ValidationException


def validate_customer_name(name):
    name = name.strip()

    if not name:
        raise ValidationException("Customer name cannot be empty. ")

    if len(name) < 2:
        raise ValidationException("Customer name is too short.")
