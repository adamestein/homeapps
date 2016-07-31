from django import forms
from django.core.exceptions import ValidationError
from django.forms.models import modelformset_factory, BaseModelFormSet

from .models import Account, Income, Statement
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


class IncomeForm(forms.ModelForm):
    class Meta:
        fields = ['name', 'account_number', 'amount', 'date', 'options']
        model = Income
        widgets = {
            'options': forms.MultipleHiddenInput
        }


class EmptyIncomeFormSet(BaseModelFormSet):
    def __init__(self, *args, **kwargs):
        super(EmptyIncomeFormSet, self).__init__(*args, **kwargs)
        self.queryset = Income.objects.none()

IncomeFormSet = modelformset_factory(Income, form=IncomeForm, formset=EmptyIncomeFormSet, extra=0)


class StatementForm(forms.ModelForm):
    class Meta:
        fields = ['date']
        model = Statement

    def clean_date(self):
        if Statement.objects.filter(date=self.cleaned_data['date']).exists():
            raise ValidationError('A statement for {} already exists'.format(
                self.cleaned_data['date'].strftime('%B %d, %Y'))
            )
        else:
            return self.cleaned_data['date']


class CreateStatementMultiForm(StatementMultiForm):
    form_classes = {
        'account': AccountFormSet,
        'income': IncomeFormSet,
        'statement': StatementForm
    }
