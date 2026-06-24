from django.forms import formset_factory
from .purchase_form import PurchaseForm
from .purchase_item_form import PurchaseItemForm
from .purchase_settlement_form import PurchaseSettlementForm

PurchaseItemFormSet = formset_factory(
    PurchaseItemForm,
    extra=1,
    can_delete=True
)
