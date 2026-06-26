from django import forms
from customers.models import Customer


class CustomerForm(forms.ModelForm):
    def clean_name(self):
        return self.cleaned_data["name"].strip()

    def clean_phone(self):
        return self.cleaned_data["phone"].strip()

    def clean_email(self):
        return self.cleaned_data["email"].strip()

    class Meta:
        model = Customer

        fields = [
            'name',
            'phone',
            'email',
            'address',
            'notes'
        ]
