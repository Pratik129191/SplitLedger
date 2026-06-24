from django.urls import path
from products.views import *

app_name = 'products'

urlpatterns = [
    path("", product_list_view, name="product_list"),
    path("create/", product_create_view, name="product_create"),
    path("<uuid:pk>/", product_detail_view, name="product_detail"),
    path("<uuid:pk>/update/", product_update_view, name="product_update"),
]
