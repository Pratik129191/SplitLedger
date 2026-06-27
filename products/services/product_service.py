from products.models import CompanyProduct, ProductMaster
from products.validators import validate_product_name
from core.exceptions import ValidationException


class ProductService:
    @staticmethod
    def create_product_master(*, name, unit, description=""):
        validate_product_name(name)
        product, _ = ProductMaster.objects.get_or_create(
            name=name.strip(),
            unit=unit,
            defaults={
                "description": description.strip()
            }
        )
        return product

    @staticmethod
    def map_product_to_company(*, company, product_master, selling_price):
        return CompanyProduct.objects.create(
            company=company,
            product_master=product_master,
            selling_price=selling_price,
        )

    @staticmethod
    def create_product(*, company, name, unit, selling_price, description=''):
        validate_product_name(name)
        product_master, _ = ProductMaster.objects.get_or_create(
            name=name.strip(),
            unit=unit,
            defaults={
                'description': description,
            }
        )

        if CompanyProduct.objects.filter(
                company=company,
                product_master=product_master,
        ).exists():
            raise ValidationException('Product already mapped to the company.')

        company_product = CompanyProduct.objects.create(
            company=company,
            product_master=product_master,
            selling_price=selling_price,
        )
        return company_product

    @staticmethod
    def update_product(*, company_product, name, unit, selling_price, description=''):
        validate_product_name(name)

        name = name.strip()
        description = description.strip()
        product_master = company_product.product_master

        if (
                product_master.name == name
                and product_master.unit == unit
                and product_master.description == description
        ):
            company_product.selling_price = selling_price
            company_product.save()
            return company_product

        mapping_count = product_master.company_products.count()

        if mapping_count == 1:
            product_master.name = name.strip(),
            product_master.unit = unit,
            product_master.description = description.strip(),
            product_master.save()
        else:
            new_master, _ = ProductMaster.objects.get_or_create(
                name=name,
                unit=unit,
                description=description,
            )
            company_product.product_master = new_master

        company_product.selling_price = selling_price
        company_product.save()
        return company_product

    @staticmethod
    def deactivate_product(*, company_product):
        if company_product.is_active:
            company_product.is_active = False
            company_product.save()
        return company_product
