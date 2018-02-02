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
    # Can't pass the options set in the template through statement creation/update, so we'll pass the option PKs
    # in a string
    option_list = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        fields = ['name', 'account_number', 'amount', 'total', 'date', 'url']
        model = Bill
        widgets = {
            'date': forms.DateInput(format='%m/%d/%Y')
        }

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance', None)

        if instance:
            kwargs.update(
                initial={
                    'option_list': ','.join(str(pk) for pk in instance.options.all().values_list('pk', flat=True))
                }
            )

        super(BillForm, self).__init__(*args, **kwargs)


class BillFormSet(BaseModelFormSet):
    def __init__(self, *args, **kwargs):
        kwargs.update({'queryset': kwargs.pop('instance', Bill.objects.none())})
        super(BillFormSet, self).__init__(*args, **kwargs)


class IncomeForm(forms.ModelForm):
    # Can't pass the options set in the template through statement creation/update, so we'll pass the option PKs
    # in a string
    option_list = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        fields = ['name', 'account_number', 'amount', 'date']
        model = Income
        widgets = {
            'date': forms.DateInput(format='%m/%d/%Y')
        }

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance', None)

        if instance:
            kwargs.update(
                initial={
                    'option_list': ','.join(str(pk) for pk in instance.options.all().values_list('pk', flat=True))
                }
            )

        super(IncomeForm, self).__init__(*args, **kwargs)


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
                raise ValidationError(
                    'A statement for %(date)s already exists',
                    code='exists',
                    params={'date': self.cleaned_data['date'].strftime('%B %d, %Y')}
                )

        return self.cleaned_data['date']


class CreateUpdateStatementMultiForm(StatementMultiForm):
    form_classes = {
        'account': modelformset_factory(Account, form=AccountForm, formset=AccountFormSet, extra=0),
        'bill': modelformset_factory(Bill, form=BillForm, formset=BillFormSet, extra=0),
        'income': modelformset_factory(Income, form=IncomeForm, formset=IncomeFormSet, extra=0),
        'statement': StatementForm
    }
