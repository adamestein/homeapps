from django import forms

from .forms import OptionForm
from .models import AccountTemplate, BillTemplate, IncomeTemplate
from .multiform import TemplateMultiModelForm

from library.views.generic.mixins.auth import UserAndNameMixin


class CreateAccountTemplateForm(UserAndNameMixin, forms.ModelForm):
    class Meta:
        fields = ['name', 'account_number']
        model = AccountTemplate


class CreateBillTemplateForm(UserAndNameMixin, OptionForm, forms.ModelForm):
    class Meta:
        fields = ['name', 'account_number', 'amount', 'total', 'due_day', 'url', 'options', 'snap_section']
        model = BillTemplate

    def __init__(self, *args, **kwargs):
        super(CreateBillTemplateForm, self).__init__(*args, template_type='bill', **kwargs)


class CreateIncomeTemplateForm(UserAndNameMixin, OptionForm, forms.ModelForm):
    class Meta:
        fields = ['name', 'account_number', 'amount', 'arrival_day', 'options', 'snap_section']
        model = IncomeTemplate

    def __init__(self, *args, **kwargs):
        super(CreateIncomeTemplateForm, self).__init__(*args, template_type='income', **kwargs)


class TemplateTypeForm(forms.Form):
    from .template_views import TEMPLATE_CHOICES

    template_type = forms.ChoiceField(choices=(('', '---------'),) + TEMPLATE_CHOICES)


class CreateTemplateMultiForm(TemplateMultiModelForm):
    form_classes = {
        'account': CreateAccountTemplateForm,
        'bill': CreateBillTemplateForm,
        'income': CreateIncomeTemplateForm,
        'template_type': TemplateTypeForm
    }


class UpdateAccountTemplateForm(CreateAccountTemplateForm):
    class Meta(CreateAccountTemplateForm.Meta):
        fields = CreateAccountTemplateForm.Meta.fields + ['disabled']


class UpdateBillTemplateForm(CreateBillTemplateForm):
    class Meta(CreateBillTemplateForm.Meta):
        fields = CreateBillTemplateForm.Meta.fields + ['disabled']


class UpdateIncomeTemplateForm(CreateIncomeTemplateForm):
    class Meta(CreateIncomeTemplateForm.Meta):
        fields = CreateIncomeTemplateForm.Meta.fields + ['disabled']


class UpdateTemplateForm(UserAndNameMixin, forms.ModelForm):
    pass
