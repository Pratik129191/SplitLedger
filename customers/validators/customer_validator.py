from core.exceptions import ValidationException


def validate_customer_name(name):
    if name.strip() == "":
        raise ValidationException("Customer name cannot be empty ")

