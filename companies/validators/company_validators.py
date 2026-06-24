from core.exceptions import ValidationException


def validate_company_name(name):
    if not name.strip():
        raise ValidationException("Company name cannot be empty")


