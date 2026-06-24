from django.urls import path
from companies.views import *

app_name = 'companies'

urlpatterns = [
    path('', company_list_view, name='company_list'),
    path('create/', company_create_view, name='company_create'),
    path('<uuid:pk>/', company_detail_view, name='company_detail'),
    path('<uuid:pk>/update/', company_update_view, name='company_update'),
    path('<uuid:pk>/delete/', company_delete_view, name='company_delete'),
]
