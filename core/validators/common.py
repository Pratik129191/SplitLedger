from core.exceptions import ValidationException


def validate_positive_amount(value):
    if value <= 0:
        raise ValidationException('Amount must be positive')


def validate_non_empty_strings(value):
    if not value.strip():
        raise ValidationException('Value cannot be empty')

