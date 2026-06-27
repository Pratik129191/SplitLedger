from django import forms
from sales.models import SalePaymentMode


class SaleSettlementForm(forms.Form):
    amount = forms.DecimalField(
        decimal_places=2,
        min_value=0.01
    )

    payment_mode = forms.ModelChoiceField(
        queryset=SalePaymentMode.objects.none(),
    )

    reference_number = forms.CharField(
        required=False,
    )

    remarks = forms.CharField(
        required=False,
    )

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields['payment_mode'].queryset = SalePaymentMode.objects.filter(
                owner=user,
                is_active=True,
            )
