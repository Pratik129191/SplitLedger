from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404

from customers.forms import CustomerForm
from customers.models import Customer
from customers.services import (
    CustomerService,
    CustomerLedgerService,
    CustomerQueryService
)


@login_required
def customer_list_view(request):
    customers = CustomerQueryService.search(
        user=request.user,
        search=request.GET.get('search')
    )

    paginator = Paginator(customers, 10)
    page_obj = paginator.get_page(
        request.GET.get('page')
    )

    return render(
        request,
        'customers/customer_list.html',
        {
            'customers': page_obj,
        }
    )


@login_required
def customer_create_view(request):
    form = CustomerForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            try:
                CustomerService.create_customer(
                    owner=request.user,
                    **form.cleaned_data
                )
                messages.success(
                    request,
                    'Customer created successfully.'
                )
                return redirect('customers:customer_list')
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
        'customers/customer_form.html',
        {
            'form': form,
            'title': 'Create Customer'
        }
    )


@login_required
def customer_update_view(request, pk):
    customer = get_object_or_404(
        Customer,
        pk=pk,
        owner=request.user
    )
    form = CustomerForm(
        request.POST or None,
        instance=customer
    )
    if request.method == 'POST':
        if form.is_valid():
            try:
                CustomerService.update_customer(
                    customer=customer,
                    **form.cleaned_data
                )
                messages.success(
                    request,
                    'Customer updated successfully.'
                )
                return redirect('customers:customer_list')
            except Exception as e:
                messages.error(
                    request,
                    str(e)
                )
    return render(
        request,
        'customers/customer_form.html',
        {
            'form': form,
            'title': 'Edit Customer'
        }
    )


@login_required
def customer_delete_view(request, pk):
    customer = get_object_or_404(
        Customer,
        pk=pk,
        owner=request.user
    )
    CustomerService.deactivate_customer(
        customer=customer
    )
    messages.success(
        request,
        "Customer deactivated successfully."
    )
    return redirect('customers:customer_list')


@login_required
def customer_detail_view(request, pk):
    customer = get_object_or_404(
        Customer.objects.prefetch_related(
            "sales"
        ),
        pk=pk,
        owner=request.user
    )
    return render(
        request,
        'customers/customer_detail.html',
        {
            'customer': customer
        }
    )


@login_required
def customer_ledger_view(request, pk):
    customer = get_object_or_404(
        Customer,
        pk=pk,
        owner=request.user
    )

    entries = CustomerLedgerService.get_customer_ledger(
        customer
    )

    return render(
        request,
        'customers/customer_ledger.html',
        {
            'customer': customer,
            'entries': entries,
            "outstanding_amount": customer.outstanding_amount,
            "total_sales": customer.total_sales_amount,
            "total_received": customer.total_received_amount
        }
    )
