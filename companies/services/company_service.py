from companies.models import Company
from companies.validators import validate_company_name
from licensing.services import LicenseService


class CompanyService:
    @staticmethod
    def create_company(*, owner, name, legal_name="", phone="", email=""):
        LicenseService().assert_can_create_company()
        validate_company_name(name)
        return Company.objects.create(
            owner=owner,
            name=name,
            legal_name=legal_name,
            phone=phone,
            email=email
        )

    @staticmethod
    def update_company(*, company, name, legal_name="", phone="", email=""):
        validate_company_name(name)
        company.name = name
        company.legal_name = legal_name
        company.phone = phone
        company.email = email
        company.save()
        return company

    @staticmethod
    def deactivate_company(*, company):
        company.is_active = False
        company.save()
