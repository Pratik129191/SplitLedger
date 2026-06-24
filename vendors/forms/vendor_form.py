from django import forms
from vendors.models import Vendor


class VendorForm(forms.ModelForm):
    class Meta:
        model = Vendor

        fields = [
            'name',
            'phone',
            'email',
            'address',
            'notes'
        ]
