from django.urls import path

from .views import dashboard_view, reports_views

app_name = 'core'

urlpatterns = [
    path('', dashboard_view, name='dashboard'),
    path('reports/', reports_views.reports_dashboard_view, name='reports_dashboard'),
]
