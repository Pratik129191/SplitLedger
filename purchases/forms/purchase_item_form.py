from django import forms
from products.models import CompanyProduct


class PurchaseItemForm(forms.Form):
    company_product = forms.ModelChoiceField(
        queryset=CompanyProduct.objects.none()
    )

    quantity = forms.DecimalField(
        decimal_places=3,
        min_value=0.001
    )

    rate = forms.DecimalField(
        decimal_places=2,
        min_value=0.01
    )

    def clean_quantity(self):
        return self.cleaned_data['quantity']

    def clean_rate(self):
        return self.cleaned_data['rate']

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['company_product'].queryset = CompanyProduct.objects.select_related(
            'product_master', 'company'
        ).filter(
            company__owner=user,
            is_active=True
        )
