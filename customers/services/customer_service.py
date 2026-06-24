from customers.models import Customer
from customers.validators import validate_customer_name


class CustomerService:
    @staticmethod
    def create_customer(*, owner, name, phone="", email="", address="", notes=""):
        validate_customer_name(name)
        return Customer.objects.create(
            owner=owner,
            name=name,
            phone=phone,
            email=email,
            address=address,
            notes=notes,
        )

    @staticmethod
    def update_customer(*, customer, name, phone="", email="", address="", notes=""):
        validate_customer_name(name)
        customer.name = name
        customer.phone = phone
        customer.email = email
        customer.address = address
        customer.notes = notes
        customer.save()
        return customer

    @staticmethod
    def deactivate_customer(*, customer):
        customer.is_active = False
        customer.save()
       