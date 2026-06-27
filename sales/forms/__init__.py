from django.forms import formset_factory

from .sale_form import SaleForm
from .sale_item_form import SaleItemForm
from .sale_settlement_form import SaleSettlementForm

SaleItemFormSet = formset_factory(
    SaleItemForm,
    extra=1,
    can_delete=True,
)
