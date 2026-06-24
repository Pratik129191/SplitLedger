from core.exceptions import ValidationException


def validate_product_name(name):
    if not name.strip():
        raise ValidationException('Product name cannot be empty')

