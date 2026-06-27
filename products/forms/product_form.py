from django import forms

from companies.models import Company
from products.models import ProductMaster, CompanyProduct


class ProductForm(forms.ModelForm):
    company = forms.ModelChoiceField(
        queryset=Company.objects.none()
    )

    name = forms.CharField(
        max_length=250
    )

    unit = forms.ChoiceField(
        choices=ProductMaster._meta.get_field("unit").choices
    )

    description = forms.CharField(
        required=False,
        widget=forms.Textarea
    )

    class Meta:
        model = CompanyProduct
        fields = (
            "company",
            "selling_price"
        )

    def clean_name(self):
        return self.cleaned_data["name"].strip()

    def clean_description(self):
        return self.cleaned_data["description"].strip()
    
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)

        if user:
            self.fields["company"].queryset = Company.objects.filter(
                owner=user,
                is_active=True
            )
