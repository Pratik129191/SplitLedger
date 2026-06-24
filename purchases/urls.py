from django.urls import path
from purchases.views import *

app_name = "purchases"

urlpatterns = [
    path('', purchase_list_view, name='purchase_list'),
    path('create/', purchase_create_view, name='purchase_create'),
    path("<uuid:pk>/", purchase_detail_view, name='purchase_detail'),
    path("<uuid:pk>/update/", purchase_update_view, name="purchase_update"),
    path("<uuid:pk>/cancel/", purchase_cancel_view, name="purchase_cancel"),
    path("<uuid:pk>/settlement/", purchase_settlement_view, name="purchase_settlement"),

]
