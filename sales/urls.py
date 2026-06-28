from django.urls import path, include
from .views import *

app_name = 'sales'

urlpatterns = [
    path('api/', include('sales.api.urls')),
    path('', sale_list_view, name='sale_list'),
    path('create/', sale_create_view, name='sale_create'),
    path('<uuid:pk>/', sale_detail_view, name='sale_detail'),
    path('<uuid:pk>/update/', sale_update_view, name='sale_update'),
    path('<uuid:pk>/cancel/', sale_cancel_view, name='sale_cancel'),
    path('<uuid:pk>/settlement/', sale_settlement_view, name='sale_settlement'),
    path('<uuid:pk>/return/', sale_return_view, name='sale_return'),
]
