from django.urls import path
from .views import *

urlpatterns = [
    path('available-companies/', available_companies_view, name='available_companies_api'),
    path('resolve-product/', resolve_company_product_view, name='resolve_company_product_api'),
]
