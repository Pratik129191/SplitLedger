from vendors.models import Vendor
from vendors.validators import validate_vendor_name
from core.exceptions import ValidationException


class VendorService:
    @staticmethod
    def create_vendor(*, owner, name, phone="", email="", address="", notes=""):
        validate_vendor_name(name)
        if Vendor.objects.filter(
                owner=owner,
                name=name.strip(),
        ).exists():
            raise ValidationException('Vendor already exists')

        return Vendor.objects.create(
            owner=owner,
            name=name.strip(),
            phone=phone.strip(),
            email=email.strip(),
            address=address.strip(),
            notes=notes.strip(),
        )

    @staticmethod
    def update_vendor(*, vendor, name, phone='', email='', address='', notes=''):
        validate_vendor_name(name)

        vendor.name = name.strip()
        vendor.phone = phone.strip()
        vendor.email = email.strip()
        vendor.address = address.strip()
        vendor.notes = notes.strip()
        vendor.save()
        return vendor

    @staticmethod
    def deactivate_vendor(*, vendor):
        if vendor.is_active:
            vendor.is_active = False
            vendor.save()
        return vendor
