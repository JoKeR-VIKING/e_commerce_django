from django import forms
from payment.models import ShippingAddress

class ShippingForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = ['full_name', 'address1', 'address2', 'city', 'state', 'zipcode']
        exclude = ['user',]

    def __init__(self, *args, **kwargs):
        super(ShippingForm, self).__init__(*args, **kwargs)

        self.fields['full_name'].widget.attrs['placeholder'] = 'Full name'
        self.fields['address1'].widget.attrs['placeholder'] = 'Address1'
        self.fields['address2'].widget.attrs['placeholder'] = 'Address2'
        self.fields['city'].widget.attrs['placeholder'] = 'City'
        self.fields['state'].widget.attrs['placeholder'] = 'State'
        self.fields['zipcode'].widget.attrs['placeholder'] = 'Zip Code'
