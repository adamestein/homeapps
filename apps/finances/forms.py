from tekextensions.widgets import MultipleSelectWithPopUp

from django import forms

from .models import AccountTemplate, BillTemplate, IncomeTemplate, Option
from .multiform import FinancesMultiModelForm

from library.views.generic.mixins.auth import UserAndNameMixin


class OptionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        template_type = kwargs.pop('template_type', None)

        super(OptionForm, self).__init__(*args, **kwargs)

        if template_type:
            self.fields['options'] = forms.ModelMultipleChoiceField(
                help_text='Options for the {}.'.format(template_type),
                queryset=Option.objects.filter(template_type=template_type),
                required=False,
                widget=MultipleSelectWithPopUp(model='Option')
            )
            self.fields['options'].label_from_instance = self.option_label_from_instance

    @staticmethod
    def option_label_from_instance(obj):
        from django.utils.encoding import smart_text
        return smart_text(obj.short_label)


class CreateAccountTemplateForm(UserAndNameMixin, forms.ModelForm):
    class Meta:
        fields = ['name', 'account_number']
        model = AccountTemplate


class CreateBillTemplateForm(UserAndNameMixin, OptionForm, forms.ModelForm):
    class Meta:
        fields = ['name', 'account_number', 'amount', 'total', 'due_day', 'url', 'options']
        model = BillTemplate

    def __init__(self, *args, **kwargs):
        super(CreateBillTemplateForm, self).__init__(*args, template_type='bill', **kwargs)


class CreateIncomeTemplateForm(UserAndNameMixin, OptionForm, forms.ModelForm):
    class Meta:
        fields = ['name', 'account_number', 'amount', 'arrival_day', 'options']
        model = IncomeTemplate

    def __init__(self, *args, **kwargs):
        super(CreateIncomeTemplateForm, self).__init__(*args, template_type='income', **kwargs)


class TemplateTypeForm(forms.Form):
    from .templates import TEMPLATE_CHOICES

    template_type = forms.ChoiceField(choices=(('', '---------'),) + TEMPLATE_CHOICES)


class CreateTemplateMultiForm(FinancesMultiModelForm):
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
