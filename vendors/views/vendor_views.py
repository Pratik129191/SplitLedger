from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404

from vendors.forms import VendorForm
from vendors.models import Vendor
from vendors.services import (
    VendorService,
    VendorLedgerService,
    VendorQueryService
)


@login_required
def vendor_list_view(request):
    vendors = VendorQueryService.search(
        user=request.user,
        search=request.GET.get('search')
    )

    paginator = Paginator(vendors, 10)

    page_obj = paginator.get_page(
        request.GET.get('page')
    )

    return render(
        request,
        'vendors/vendor_list.html',
        {
            'vendors': page_obj,
        }
    )


@login_required
def vendor_create_view(request):
    form = VendorForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            VendorService.create_vendor(
                owner=request.user,
                **form.cleaned_data
            )
            messages.success(
                request,
                'Vendor created successfully.'
            )
            return redirect(
                'vendors:vendor_list'
            )
    return render(
        request,
        'vendors/vendor_form.html',
        {
            'form': form,
            'title': 'Create Vendor'
        }
    )


@login_required
def vendor_update_view(request, pk):
    vendor = get_object_or_404(
        Vendor,
        pk=pk,
        owner=request.user
    )
    form = VendorForm(
        request.POST or None,
        instance=vendor
    )
    if request.method == 'POST':
        if form.is_valid():
            VendorService.update_vendor(
                vendor=vendor,
                **form.cleaned_data
            )
            messages.success(
                request,
                'Vendor updated successfully.'
            )
            return redirect(
                'vendors:vendor_list'
            )
    return render(
        request,
        'vendors/vendor_form.html',
        {
            'form': form,
            'title': 'Edit Vendor'
        }
    )


@login_required
def vendor_delete_view(request, pk):
    vendor = get_object_or_404(
        Vendor,
        pk=pk,
        owner=request.user
    )
    VendorService.deactivate_vendor(
        vendor=vendor
    )
    return redirect(
        'vendors:vendor_list'
    )


@login_required
def vendor_detail_view(request, pk):
    vendor = get_object_or_404(
        Vendor,
        pk=pk,
        owner=request.user
    )
    return render(
        request,
        'vendors/vendor_detail.html',
        {
            'vendor': vendor
        }
    )


@login_required
def vendor_ledger_view(request, pk):
    vendor = get_object_or_404(
        Vendor,
        pk=pk,
        owner=request.user
    )
    entries = VendorLedgerService.get_vendor_ledger(
        vendor
    )

    return render(
        request,
        'vendors/vendor_ledger.html',
        {
            'vendor': vendor,
            'entries': entries
        }
    )
