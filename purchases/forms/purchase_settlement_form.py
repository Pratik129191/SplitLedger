from django import forms
from purchases.models import PurchasePaymentMode


class PurchaseSettlementForm(forms.Form):
    amount = forms.DecimalField(
        decimal_places=2,
        min_value=0.01
    )

    payment_mode = forms.ModelChoiceField(
        queryset=PurchasePaymentMode.objects.none(),
    )

    reference_number = forms.CharField(
        required=False
    )

    remarks = forms.CharField(
        required=False,
        widget=forms.Textarea
    )

    def clean_reference_number(self):
        return self.cleaned_data['reference_number'].strip()

    def clean_remarks(self):
        return self.cleaned_data['remarks'].strip()

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields['payment_mode'].queryset = PurchasePaymentMode.objects.filter(
                owner=user,
                is_active=True
            )
