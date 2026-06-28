from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from products.models import ProductMaster
from products.services import ProductResolutionService


@login_required
def available_companies_view(request):
    product_master_id = request.GET.get('product')
    if not product_master_id:
        return JsonResponse({
            'success': False,
            'message': 'Product is required.'
        })

    try:
        product_master = ProductMaster.objects.get(
            id=product_master_id,
            is_active=True
        )
    except ProductMaster.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Invalid product.'
        })

    mappings = ProductResolutionService.get_available_companies(
        owner=request.user,
        product_master=product_master
    )

    companies = []
    for mapping in mappings:
        companies.append({
            'id': str(mapping.id),
            'name': str(mapping.company.name)
        })
    return JsonResponse({
        'success': True,
        'companies': companies
    })


@login_required
def resolve_company_product_view(request):
    product_master_id = request.GET.get('product')
    company_id = request.GET.get('company')

    if not product_master_id:
        return JsonResponse({
            'success': False,
            'message': 'Product is required.'
        })

    try:
        product_master = ProductMaster.objects.get(
            id=product_master_id,
            is_active=True
        )
    except ProductMaster.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Invalid product.'
        })

    company = None
    if company_id:
        from companies.models import Company
        try:
            company = Company.objects.get(
                id=company_id,
                owner=request.user,
                is_active=True
            )
        except Company.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Invalid company.'
            })

    try:
        company_product = ProductResolutionService.resolve_product(
            owner=request.user,
            product_master=product_master,
            company=company
        )
    except Exception as exc:
        return JsonResponse({
            'success': False,
            'message': str(exc)
        })

    stock = getattr(company_product, 'stock', None)
    
    return JsonResponse({
        'success': True,
        'company_product': str(company_product.id),
        'company': {
            'id': str(company_product.company.id),
            'name': str(company_product.company.name)
        },
        'product': {
            'id': str(company_product.product_master.id),
            'name': str(company_product.product_master.name),
            'unit': str(company_product.product_master.unit)
        },
        'selling_price': float(company_product.selling_price),
        'stock': float(stock.quantity if stock else 0)
    })
