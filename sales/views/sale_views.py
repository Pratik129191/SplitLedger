from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from sales.forms import (
    SaleForm,
    SaleItemFormSet,
    SaleSettlementForm,
)
from sales.models import MasterSale
from sales.services import (
    SaleSearchService,
    SaleService,
    SettlementService,
    ReturnService,
)


@login_required
def sale_list_view(request):
    sales = SaleSearchService.search(
        user=request.user,
        invoice_number=request.GET.get("search"),
    )
    paginator = Paginator(sales, 10)
    page_obj = paginator.get_page(request.GET.get("page"))
    return render(
        request,
        'sales/sale_list.html',
        {
            'sales': page_obj
        }
    )


@login_required
def sale_create_view(request):
    form = SaleForm(
        request.POST or None,
        user=request.user,
    )
    item_formset = SaleItemFormSet(
        request.POST or None,
        form_kwargs={
            'user': request.user,
        }
    )

    if request.method == "POST":
        if form.is_valid() and item_formset.is_valid():
            items = []
            for row in item_formset:
                if not row.cleaned_data:
                    continue
                if row.cleaned_data.get('DELETE'):
                    continue
                items.append(
                    {
                        'product_master': row.cleaned_data['product_master'],
                        'company': row.cleaned_data['company'],
                        'quantity': row.cleaned_data['quantity'],
                    }
                )

            try:
                sale = SaleService.create_sale(
                    owner=request.user,
                    customer=form.cleaned_data['customer'],
                    notes=form.cleaned_data['notes'],
                    items=items,
                )
                messages.success(
                    request,
                    f'Sale {sale.invoice_number} created successfully.'
                )
                return redirect('sales:sale_detail', sale.id)
            except Exception as e:
                messages.error(
                    request,
                    str(e)
                )

    return render(
        request,
        'sales/sale_form.html',
        {
            'form': form,
            'item_formset': item_formset,
            'title': 'Create Sale'
        }
    )


@login_required
def sale_detail_view(request, pk):
    sale = get_object_or_404(
        MasterSale.objects.select_related(
            "customer"
        ).prefetch_related(
            "items",
            "company_sales",
            "settlements",
            "returns",
        ),
        pk=pk,
        owner=request.user,
    )

    return render(
        request,
        "sales/sale_detail.html",
        {
            "sale": sale,
        },
    )


@login_required
def sale_update_view(request, pk):
    sale = get_object_or_404(
        MasterSale,
        pk=pk,
        owner=request.user,
    )

    form = SaleForm(
        request.POST or None,
        user=request.user,
        initial={
            "customer": sale.customer,
            "notes": sale.notes,
        },
    )

    initial_items = []
    for item in sale.items.select_related(
            "company_product",
            "company_product__product_master",
            "company_product__company",
    ):
        initial_items.append(
            {
                "product_master": item.company_product.product_master,
                "company": item.company_product.company,
                "quantity": item.quantity,
            }
        )

    item_formset = SaleItemFormSet(
        request.POST or None,
        initial=initial_items,
        form_kwargs={
            "user": request.user
        },
    )

    if request.method == "POST":
        if form.is_valid() and item_formset.is_valid():

            items = []
            for row in item_formset:
                if not row.cleaned_data:
                    continue

                if row.cleaned_data.get("DELETE"):
                    continue

                items.append(
                    {
                        "product_master": row.cleaned_data["product_master"],
                        "company": row.cleaned_data["company"],
                        "quantity": row.cleaned_data["quantity"],
                    }
                )

            try:
                SaleService.update_sale(
                    sale=sale,
                    customer=form.cleaned_data["customer"],
                    notes=form.cleaned_data["notes"],
                    items=items,
                )
                messages.success(
                    request,
                    "Sale updated successfully."
                )
                return redirect(
                    "sales:sale_detail",
                    sale.id,
                )
            except Exception as exc:
                messages.error(
                    request,
                    str(exc)
                )
    return render(
        request,
        "sales/sale_form.html",
        {
            "form": form,
            "item_formset": item_formset,
            "title": f"Edit {sale.invoice_number}",
        },
    )


@login_required
def sale_cancel_view(request, pk):
    sale = get_object_or_404(
        MasterSale,
        pk=pk,
        owner=request.user,
    )
    try:
        SaleService.cancel_sale(
            sale=sale
        )
        messages.success(
            request,
            "Sale cancelled successfully."
        )
    except Exception as exc:
        messages.error(
            request,
            str(exc)
        )
    return redirect(
        "sales:sale_detail",
        sale.id,
    )


@login_required
def sale_settlement_view(request, pk):
    sale = get_object_or_404(
        MasterSale.objects.select_related(
            "customer"
        ),
        pk=pk,
        owner=request.user,
    )
    form = SaleSettlementForm(
        request.POST or None,
        user=request.user,
        initial={
            "amount":
                sale.outstanding_amount
        },
    )
    if request.method == "POST":
        if form.is_valid():
            try:
                SettlementService.create_settlement(
                    sale=sale,
                    amount=form.cleaned_data["amount"],
                    payment_mode=form.cleaned_data["payment_mode"],
                    reference_number=form.cleaned_data["reference_number"],
                    remarks=form.cleaned_data["remarks"],
                )
                messages.success(
                    request,
                    "Payment recorded successfully."
                )
                return redirect(
                    "sales:sale_detail",
                    sale.id,
                )
            except Exception as exc:
                messages.error(
                    request,
                    str(exc)
                )
    return render(
        request,
        "sales/sale_settlement.html",
        {
            "sale": sale,
            "form": form,
        },
    )


@login_required
def sale_return_view(request, pk):
    sale = get_object_or_404(
        MasterSale.objects.prefetch_related(
            "items"
        ),
        pk=pk,
        owner=request.user,
    )
    if request.method == "POST":
        messages.info(
            request,
            "Sale Return UI will be implemented next."
        )
    return render(
        request,
        "sales/sale_return.html",
        {
            "sale": sale,
        },
    )
