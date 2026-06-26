from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib.auth.decorators import login_required
from companies.forms import CompanyForm
from companies.models import Company
from companies.services import CompanyService, CompanyQueryService


@login_required
def company_list_view(request):
    companies = CompanyQueryService.search(
        user=request.user,
        search=request.GET.get('search'),
    )

    paginator = Paginator(companies, 10)
    page_obj = paginator.get_page(
        request.GET.get('page'),
    )
    context = {
        'companies': page_obj,
        'create_url': reverse('companies:company_create'),
        'search': request.GET.get('search', ''),
    }
    return render(
        request,
        'companies/company_list.html',
        context
    )


@login_required
def company_create_view(request):
    form = CompanyForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            try:
                CompanyService.create_company(
                    owner=request.user,
                    **form.cleaned_data
                )
                messages.success(
                    request,
                    'Company created successfully.'
                )
                return redirect('companies:company_list')
            except Exception as e:
                messages.error(
                    request,
                    str(e)
                )
        else:
            messages.error(
                request,
                "Please correct the errors below."
            )
    return render(
        request,
        'companies/company_form.html',
        {
            'form': form,
            'title': 'Create New Company',
        }
    )


@login_required
def company_update_view(request, pk):
    company = get_object_or_404(
        Company,
        pk=pk,
        owner=request.user,
    )
    form = CompanyForm(
        request.POST or None,
        instance=company
    )

    if request.method == "POST":
        if form.is_valid():
            try:
                CompanyService.update_company(
                    company=company,
                    **form.cleaned_data
                )
                messages.success(
                    request,
                    'Company updated successfully.'
                )
                return redirect('companies:company_list')
            except Exception as e:
                messages.error(
                    request,
                    str(e)
                )
        else:
            messages.error(
                request,
                "Please correct the errors below."
            )
    return render(
        request,
        'companies/company_form.html',
        {
            'form': form,
            'title': 'Edit Company',
        }
    )


@login_required
def company_delete_view(request, pk):
    company = get_object_or_404(
        Company,
        pk=pk,
        owner=request.user,
    )
    CompanyService.deactivate_company(
        company=company
    )
    messages.success(
        request,
        "Company deactivated successfully."
    )
    return redirect('companies:company_list')


@login_required
def company_detail_view(request, pk):
    company = get_object_or_404(
        Company.objects.prefetch_related(
            "company_products",
            "purchases",
            "company_sales"
        ),
        pk=pk,
        owner=request.user,
    )
    return render(
        request,
        'companies/company_detail.html',
        {
            'company': company,
        }
    )
