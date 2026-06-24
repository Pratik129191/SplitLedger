from products.models import CompanyProduct, ProductMaster
from products.validators import validate_product_name


class ProductService:
    @staticmethod
    def create_product_master(*, name, unit, description=""):
        validate_product_name(name)
        return ProductMaster.objects.create(
            name=name,
            unit=unit,
            description=description,
        )

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
            defaults={
                'unit': unit,
                'description': description,
            }
        )

        company_product = CompanyProduct.objects.create(
            company=company,
            product_master=product_master,
            selling_price=selling_price,
        )
        return company_product

    @staticmethod
    def update_product(*, company_product, name, unit, selling_price, description=''):
        validate_product_name(name)
        product_master = company_product.product_master

        product_master.name = name,
        product_master.unit = unit,
        product_master.description = description,
        product_master.save()

        company_product.selling_price = selling_price
        company_product.save()
        return company_product

    @staticmethod
    def deactivate_product(*, company_product):
        company_product.is_active = False
        company_product.save()
