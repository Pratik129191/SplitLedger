from decimal import Decimal
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from purchases.forms import (
    PurchaseForm,
    PurchaseItemFormSet,
    PurchaseSettlementForm
)
from purchases.models import Purchase
from purchases.services import (
    PurchaseService,
    PurchaseSettlementService,
    PurchaseQueryService
)


@login_required
def purchase_list_view(request):
    purchases = PurchaseQueryService.search(
        user=request.user,
        search=request.GET.get('search'),
    )
    paginator = Paginator(purchases, 10)
    page_obj = paginator.get_page(
        request.GET.get('page'),
    )
    return render(
        request,
        'purchases/purchase_list.html',
        {
            'purchases': page_obj,
        }
    )


@login_required
def purchase_create_view(request):
    form = PurchaseForm(
        request.POST or None,
        user=request.user,
    )
    item_formset = PurchaseItemFormSet(
        request.POST or None,
        form_kwargs={
            'user': request.user,
        }
    )

    if request.method == 'POST':
        if form.is_valid() and item_formset.is_valid():
            items = []
            for row in item_formset:
                if not row.cleaned_data:
                    continue
                if row.cleaned_data.get('DELETE'):
                    continue

                items.append(
                    {
                        'company_product': row.cleaned_data['company_product'],
                        'quantity': row.cleaned_data['quantity'],
                        'rate': row.cleaned_data['rate'],
                    }
                )

            purchase = PurchaseService.create_purchase(
                company=form.cleaned_data['company'],
                vendor=form.cleaned_data['vendor'],
                notes=form.cleaned_data['notes'],
                items=items
            )
            messages.success(
                request,
                f'Purchase {purchase.invoice_number} created successfully.'
            )
            return redirect(
                'purchases:purchase_detail',
                purchase.id
            )

    return render(
        request,
        'purchases/purchase_form.html',
        {
            'form': form,
            'item_formset': item_formset,
            'title': 'Create Purchase',
        }
    )


@login_required
def purchase_detail_view(request, pk):
    purchase = get_object_or_404(
        Purchase.objects.select_related(
            'company', 'vendor'
        ),
        pk=pk,
        company__owner=request.user
    )
    return render(
        request,
        'purchases/purchase_detail.html',
        {
            'purchase': purchase,
        }
    )


@login_required
def purchase_cancel_view(request, pk):
    purchase = get_object_or_404(
        Purchase,
        pk=pk,
        company__owner=request.user
    )
    PurchaseService.cancel_purchase(
        purchase=purchase
    )
    messages.success(
        request,
        'Purchase cancelled successfully.'
    )
    return redirect(
        'purchases:purchase_detail',
        purchase.id
    )


@login_required
def purchase_update_view(request, pk):
    purchase = get_object_or_404(
        Purchase,
        pk=pk,
        company__owner=request.user
    )
    form = PurchaseForm(
        request.POST or None,
        user=request.user,
        initial={
            'company': purchase.company,
            'vendor': purchase.vendor,
            'notes': purchase.notes
        }
    )
    initial_items = [
        {
            'company_product': item.company_product,
            'quantity': item.quantity,
            'rate': item.rate_snapshot,
        }
        for item in purchase.items.select_related('company_product')
    ]
    item_formset = PurchaseItemFormSet(
        request.POST or None,
        initial=initial_items,
        form_kwargs={
            'user': request.user,
        }
    )

    if request.method == 'POST':
        if form.is_valid() and item_formset.is_valid():
            items = []
            for row in item_formset:
                if not row.cleaned_data:
                    continue
                if row.cleaned_data.get('DELETE'):
                    continue
                items.append(
                    {
                        'company_product': row.cleaned_data['company_product'],
                        'quantity': row.cleaned_data['quantity'],
                        'rate': row.cleaned_data['rate'],
                    }
                )
            PurchaseService.update_purchase(
                purchase=purchase,
                vendor=form.cleaned_data['vendor'],
                notes=form.cleaned_data['notes'],
                items=items
            )
            messages.info(
                request,
                'Purchase edit will be implemented in phase 11.3'
            )
            return redirect(
                'purchases:purchase_detail',
                purchase.id
            )

    return render(
        request,
        'purchases/purchase_form.html',
        {
            'form': form,
            'item_formset': item_formset,
            'title': f'Edit {purchase.invoice_number}',
        }
    )


@login_required
def purchase_settlement_view(request, pk):
    purchase = get_object_or_404(
        Purchase.objects.select_related(
            'vendor', 'company'
        ),
        pk=pk,
        company__owner=request.user
    )
    form = PurchaseSettlementForm(
        request.POST or None,
        user=request.user,
        initial={
            'amount': purchase.outstanding_amount,
        }
    )
    if request.method == 'POST':
        if form.is_valid():
            try:
                PurchaseSettlementService.create_settlement(
                    purchase=purchase,
                    amount=form.cleaned_data['amount'],
                    payment_mode=form.cleaned_data['payment_mode'],
                    reference_number=form.cleaned_data['reference_number'],
                    remarks=form.cleaned_data['remarks']
                )
                messages.success(
                    request,
                    'Payment recorded successfully.'
                )
                return redirect(
                    'purchases:purchase_detail',
                    purchase.id,
                )
            except Exception as e:
                messages.error(
                    request,
                    str(e)
                )
    return render(
        request,
        'purchases/purchase_settlement.html',
        {
            'purchase': purchase,
            'form': form,
        }
    )
