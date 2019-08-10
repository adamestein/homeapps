from django import forms

from .models import Bill


class TrackerBillForm(forms.ModelForm):
    has_auto_pay = forms.BooleanField(widget=forms.HiddenInput(), required=False)
    pk = forms.IntegerField(widget=forms.HiddenInput())

    class Meta:
        fields = ['actual', 'paid_date', 'payment_method', 'check_number', 'confirmation_number', 'url']
        model = Bill
        widgets = {
            'paid_date': forms.DateInput(format='%m/%d/%Y'),
            'url': forms.HiddenInput
        }

    def __init__(self, *args, **kwargs):
        super(TrackerBillForm, self).__init__(*args, **kwargs)

        # Set initial value for has_auto_pay to the instance's has_auto_pay property
        self.fields['has_auto_pay'].initial = self.instance.has_auto_pay

        # Set initial value for pk to the instance's ID (for some reason, can't get 'id' to show up in form on it's own)
        self.fields['pk'].initial = self.instance.id

    def clean(self):
        cleaned_data = super(TrackerBillForm, self).clean()

        used_check = 'payment_method' in cleaned_data and cleaned_data['payment_method'] == Bill.PAYMENT_METHOD_CHECK
        if used_check and cleaned_data['check_number'] is None:
            # If payment is by check, need to specify the check number
            self.add_error('check_number', 'Need to specify the number')

