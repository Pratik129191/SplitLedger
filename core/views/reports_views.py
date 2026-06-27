from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def reports_dashboard_view(request):
    return render(request, "reports/reports_dashboard.html")
