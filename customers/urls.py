from django.urls import path
from customers.views import *

app_name = 'customers'

urlpatterns = [
    path('', customer_list_view, name='customer_list'),
    path('create/', customer_create_view, name='customer_create'),
    path('<uuid:pk>/', customer_detail_view, name='customer_detail'),
    path('<uuid:pk>/update/', customer_update_view, name='customer_update'),
    path('<uuid:pk>/delete/', customer_delete_view, name='customer_delete'),
    path('<uuid:pk>/ledger/', customer_ledger_view, name='customer_ledger'),
]
