from django import forms
from customers.models import Customer


class SaleForm(forms.Form):
    customer = forms.ModelChoiceField(
        queryset=Customer.objects.none(),
        required=False,
    )

    notes = forms.CharField(
        required=False,
        widget=forms.Textarea,
    )

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields['customer'].queryset = Customer.objects.filter(
                owner=user,
                is_active=True,
            )
            