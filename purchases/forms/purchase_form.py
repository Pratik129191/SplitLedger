from django import forms
from companies.models import Company
from vendors.models import Vendor


class PurchaseForm(forms.Form):
    company = forms.ModelChoiceField(
        queryset=Company.objects.none(),
    )

    vendor = forms.ModelChoiceField(
        queryset=Vendor.objects.none(),
    )

    notes = forms.CharField(
        required=False,
        widget=forms.Textarea,
    )

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields['company'].queryset = Company.objects.filter(
                owner=user,
                is_active=True
            )
            self.fields['vendor'].queryset = Vendor.objects.filter(
                owner=user,
                is_active=True
            )
