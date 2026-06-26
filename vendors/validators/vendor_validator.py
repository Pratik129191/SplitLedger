from core.exceptions import ValidationException


def validate_vendor_name(name):
    name = name.strip()

    if not name:
        raise ValidationException('Vendor name cannot be empty.')
    if len(name) < 2:
        raise ValidationException('Vendor name is too short.')
