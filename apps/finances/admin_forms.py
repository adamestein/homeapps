from django import forms

from .models import Bill


# The whole purpose of this form is to ensure that the payment_method field isn't required when viewing in the admin
# (as long as the bill isn't in the 'paid' state), whereas, in the Tracker, it would still remain required (regardless
# of state)
class AdminBillForm(forms.ModelForm):
    class Meta:
        model = Bill

    def __init__(self, *args, **kwargs):
        super(AdminBillForm, self).__init__(*args, **kwargs)
        self.fields['payment_method'].required = False

    def clean(self):
        cleaned_data = super(AdminBillForm, self).clean()

        payment_method_set = 'payment_method' in cleaned_data and cleaned_data['payment_method']
        if cleaned_data['state'] == Bill.STATE_PAID and not payment_method_set:
            # Error if the bill is in the paid state but no payment method is specified
            self._errors['payment_method'] = self.error_class(
                ['Need to specify a payment method when in the paid state']
            )
            del cleaned_data['payment_method']

        return cleaned_data
