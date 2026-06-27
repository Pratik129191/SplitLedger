from django.shortcuts import render
from django.contrib import messages
from inventory.services import StockQueryService
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required


@login_required
def stock_list_view(request):
    try:
        stocks = StockQueryService.stock_search(
            user=request.user,
            search=request.GET.get('search'),
        )
    except Exception as e:
        messages.error(
            request,
            str(e)
        )

    paginator = Paginator(stocks, 20)
    page_obj = paginator.get_page(
        request.GET.get('page')
    )

    return render(
        request,
        'inventory/stock_list.html',
        {
            'stocks': page_obj,
            'search': request.GET.get('search'),
        }
    )


@login_required
def stock_movement_list_view(request):
    try:
        stock_movements = StockQueryService.stock_movement_search(
            user=request.user,
        )
    except Exception as e:
        messages.error(
            request,
            str(e)
        )

    paginator = Paginator(stock_movements, 20)
    page_obj = paginator.get_page(
        request.GET.get('page')
    )
    return render(
        request,
        'inventory/stock_movements.html',
        {
            'stock_movements': page_obj,
            'search': request.GET.get('search'),
        }
    )
