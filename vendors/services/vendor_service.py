from vendors.models import Vendor


class VendorService:
    @staticmethod
    def create_vendor(*, owner, name, phone="", email="", address="", notes=""):
        return Vendor.objects.create(
            owner=owner,
            name=name,
            phone=phone,
            email=email,
            address=address,
            notes=notes,
        )

    @staticmethod
    def update_vendor(*, vendor, name, phone='', email='', address='', notes=''):
        vendor.name = name
        vendor.phone = phone
        vendor.email = email
        vendor.address = address
        vendor.notes = notes
        vendor.save()
        return vendor

    @staticmethod
    def deactivate_vendor(*, vendor):
        vendor.is_active = False
        vendor.save()
