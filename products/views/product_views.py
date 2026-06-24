from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from products.forms import ProductForm
from products.models import CompanyProduct
from products.services import ProductService, ProductQueryService


@login_required
def product_list_view(request):
    products = ProductQueryService.search(
        user=request.user,
        search=request.GET.get('search'),
    )
    paginator = Paginator(products, 10)
    page_obj = paginator.get_page(
        request.GET.get('page')
    )

    return render(
        request,
        'products/product_list.html',
        {
            'products': page_obj
        }
    )


@login_required
def product_detail_view(request, pk):
    product = get_object_or_404(
        CompanyProduct.objects.select_related(
            'company', 'product_master'
        ),
        pk=pk
    )
    return render(
        request,
        'products/product_detail.html',
        {
            'product': product,
        }
    )


@login_required
def product_create_view(request):
    form = ProductForm(
        request.POST or None,
        user=request.user,
    )
    if request.method == 'POST':
        if form.is_valid():
            ProductService.create_product(
                company=form.cleaned_data['company'],
                name=form.cleaned_data['name'],
                unit=form.cleaned_data['unit'],
                selling_price=form.cleaned_data['selling_price'],
                description=form.cleaned_data['description'],
            )
            messages.success(
                request,
                'Product created successfully.'
            )
            return redirect(
                'products:product_list'
            )
    return render(
        request,
        'products/product_form.html',
        {
            'form': form,
            'title': 'Create Product',
        }
    )


@login_required
def product_update_view(request, pk):
    product = get_object_or_404(
        CompanyProduct,
        pk=pk
    )
    initial = {
        'company': product.company,
        'name': product.product_master.name,
        'unit': product.product_master.unit,
        'description': product.product_master.description,
        'selling_price': product.selling_price,
    }
    form = ProductForm(
        request.POST or None,
        user=request.user,
        initial=initial,
    )

    if request.method == 'POST':
        if form.is_valid():
            ProductService.update_product(
                company_product=product,
                name=form.cleaned_data['name'],
                unit=form.cleaned_data['unit'],
                selling_price=form.cleaned_data['selling_price'],
                description=form.cleaned_data['description'],
            )
            messages.success(
                request,
                'Product updated successfully.'
            )
            return redirect(
                'products:product_list'
            )
    return render(
        request,
        'products/product_form.html',
        {
            'form': form,
            'title': 'Edit Product',
        }
    )
