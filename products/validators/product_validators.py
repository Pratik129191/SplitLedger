from core.exceptions import ValidationException


def validate_product_name(name):
    name = name.strip()
    if not name:
        raise ValidationException('Product name cannot be empty.')

    if len(name) < 2:
        raise ValidationException('Product name is too short.')
