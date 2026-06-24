from django.urls import path
from vendors.views import *

app_name = 'vendors'

urlpatterns = [

    path('', vendor_list_view, name='vendor_list'),

    path('create/', vendor_create_view, name='vendor_create'),

    path('<uuid:pk>/', vendor_detail_view, name='vendor_detail'),

    path('<uuid:pk>/update/', vendor_update_view, name='vendor_update'),

    path('<uuid:pk>/delete/', vendor_delete_view, name='vendor_delete'),

    path('<uuid:pk>/ledger/', vendor_ledger_view, name='vendor_ledger'),

]
