from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def stock_list_view(request):
    return render(request, "inventory/stock_list.html")
