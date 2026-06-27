from products.models import CompanyProduct
from core.exceptions import ValidationException


class ProductResolutionService:
    @staticmethod
    def resolve_product(*, owner, product_master, company=None):
        company_products = CompanyProduct.objects.select_related(
            'company',
            'product_master'
        ).filter(
            product_master=product_master,
            company__owner=owner,
            is_active=True,
            company__is_active=True
        )

        if not company_products.exists():
            raise ValidationException(
                'Product is not mapped to any company.'
            )

        if company_products.count() == 1:
            return company_products.first()

        if company:
            company_product = company_products.filter(
                company=company
            ).first()
            if company_product is None:
                raise ValidationException(
                    'Invalid company selection.'
                )
            return company_product

        available = []
        for mapping in company_products:
            stock = getattr(mapping, 'stock', None)
            if stock and stock.quantity > 0:
                available.append(mapping)

        if len(available) == 0:
            raise ValidationException(
                'Product is out of stock.'
            )
        if len(available) == 1:
            return available[0]

        raise ValidationException(
            'Multiple company, selection required.'
        )
