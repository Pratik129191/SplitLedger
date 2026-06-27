from django import forms
from products.models import ProductMaster
from companies.models import Company


class SaleItemForm(forms.Form):
    product_master = forms.ModelChoiceField(
        queryset=ProductMaster.objects.filter(
            is_active=True,
        ).order_by('name'),
    )

    company = forms.ModelChoiceField(
        queryset=Company.objects.none(),
        required=False,
    )

    quantity = forms.DecimalField(
        decimal_places=3,
        min_value=0.001,
    )

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields['company'].queryset = Company.objects.filter(
                owner=user,
                is_active=True,
            )
