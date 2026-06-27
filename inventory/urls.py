from django.urls import path
from .views import *

app_name = 'inventory'

urlpatterns = [
    path('', stock_list_view, name='stock_list'),
]
