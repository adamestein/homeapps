from django import forms
from django.core.exceptions import ValidationError
from django.forms.models import modelformset_factory, BaseModelFormSet

from .models import Account, Bill, Income, Statement
from .multiform import StatementMultiForm


class AccountForm(forms.ModelForm):
    class Meta:
        fields = ['name', 'account_number', 'amount']
        model = Account


class AccountFormSet(BaseModelFormSet):
    def __init__(self, *args, **kwargs):
        kwargs.update({'queryset': kwargs.pop('instance', Account.objects.none())})
        super(AccountFormSet, self).__init__(*args, **kwargs)


class BillForm(forms.ModelForm):
    class Meta:
        fields = ['name', 'account_number', 'amount', 'total', 'date', 'url', 'options']
        model = Bill
        widgets = {
            'date': forms.DateInput(format='%m/%d/%Y'),
            'options': forms.MultipleHiddenInput
        }


class BillFormSet(BaseModelFormSet):
    def __init__(self, *args, **kwargs):
        kwargs.update({'queryset': kwargs.pop('instance', Bill.objects.none())})
        super(BillFormSet, self).__init__(*args, **kwargs)


class IncomeForm(forms.ModelForm):
    class Meta:
        fields = ['name', 'account_number', 'amount', 'date', 'options']
        model = Income
        widgets = {
            'date': forms.DateInput(format='%m/%d/%Y'),
            'options': forms.MultipleHiddenInput
        }


class IncomeFormSet(BaseModelFormSet):
    def __init__(self, *args, **kwargs):
        kwargs.update({'queryset': kwargs.pop('instance', Income.objects.none())})
        super(IncomeFormSet, self).__init__(*args, **kwargs)


class StatementForm(forms.ModelForm):
    class Meta:
        fields = ['date']
        model = Statement
        widgets = {
            'date': forms.DateInput(format='%m/%d/%Y')
        }

    def clean_date(self):
        if self.instance.id is None:
            if Statement.objects.filter(date=self.cleaned_data['date']).exists():
                raise ValidationError('A statement for {} already exists'.format(
                    self.cleaned_data['date'].strftime('%B %d, %Y'))
                )

        return self.cleaned_data['date']


class CreateUpdateStatementMultiForm(StatementMultiForm):
    form_classes = {
        'account': modelformset_factory(Account, form=AccountForm, formset=AccountFormSet, extra=0),
        'bill': modelformset_factory(Bill, form=BillForm, formset=BillFormSet, extra=0),
        'income': modelformset_factory(Income, form=IncomeForm, formset=IncomeFormSet, extra=0),
        'statement': StatementForm
    }
