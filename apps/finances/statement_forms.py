from betterforms.multiform import MultiModelForm

from django import forms
from django.forms.models import modelformset_factory, BaseModelFormSet

from .models import Account, Statement
from .multiform import StatementMultiForm


class AccountForm(forms.ModelForm):
    class Meta:
        fields = ['name', 'account_number', 'amount']
        model = Account


class EmptyAccountFormSet(BaseModelFormSet):
    def __init__(self, *args, **kwargs):
        super(EmptyAccountFormSet, self).__init__(*args, **kwargs)
        self.queryset = Account.objects.none()

AccountFormSet = modelformset_factory(Account, form=AccountForm, formset=EmptyAccountFormSet, extra=0)


class StatementForm(forms.ModelForm):
    class Meta:
        fields = ['date']
        model = Statement


class CreateStatementMultiForm(StatementMultiForm):
    form_classes = {
        'account': AccountFormSet,
        'statement': StatementForm
    }
