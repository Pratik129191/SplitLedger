from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def sale_list_view(request):
    return render(request, "sales/sale_list.html")

@login_required
def sale_create_view(request):
    return render(request, "sales/sale_create.html")
