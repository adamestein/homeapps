from django import forms

from .models import AccountTemplate, BillTemplate
from .multiform import FinancesMultiModelForm

from library.views.generic.mixins.auth import UserAndNameMixin


class CreateAccountTemplateForm(UserAndNameMixin, forms.ModelForm):
    class Meta:
        fields = ['name', 'account_number']
        model = AccountTemplate


class CreateBillTemplateForm(UserAndNameMixin, forms.ModelForm):
    class Meta:
        fields = ['name', 'account_number', 'amount', 'total', 'due_day', 'url']
        model = BillTemplate


class TemplateTypeForm(forms.Form):
    type_choices = (
        ('', '---------'),
        ('account', 'Account'),
        ('bill', 'Bill')
    )

    template_type = forms.ChoiceField(choices=type_choices)


class UpdateAccountTemplateForm(UserAndNameMixin, forms.ModelForm):
    class Meta:
        fields = ['name', 'account_number', 'disabled']
        model = AccountTemplate


class UpdateBillTemplateForm(UserAndNameMixin, forms.ModelForm):
    class Meta:
        fields = ['name', 'account_number', 'amount', 'total', 'due_day', 'url', 'disabled']
        model = BillTemplate


class CreateTemplateMultiForm(FinancesMultiModelForm):
    form_classes = {
        'account': CreateAccountTemplateForm,
        'bill': CreateBillTemplateForm,
        'template_type': TemplateTypeForm
    }


class UpdateTemplateForm(UserAndNameMixin, forms.ModelForm):
    pass
