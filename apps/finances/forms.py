from tekextensions.widgets import MultipleSelectWithPopUp

from django import forms

from .models import AccountTemplate, BillTemplate, Option
from .multiform import FinancesMultiModelForm

from library.views.generic.mixins.auth import UserAndNameMixin


class CreateAccountTemplateForm(UserAndNameMixin, forms.ModelForm):
    class Meta:
        fields = ['name', 'account_number']
        model = AccountTemplate


class CreateBillTemplateForm(UserAndNameMixin, forms.ModelForm):
    class Meta:
        fields = ['name', 'account_number', 'amount', 'total', 'due_day', 'url', 'options']
        model = BillTemplate

    def __init__(self, *args, **kwargs):
        super(CreateBillTemplateForm, self).__init__(*args, **kwargs)
        self.fields['options'] = forms.ModelMultipleChoiceField(
            help_text='Options for the bill.',
            queryset=Option.objects.filter(template_type='bill'),
            required=False,
            widget=MultipleSelectWithPopUp(model='Option')
        )
        self.fields['options'].label_from_instance = self.option_label_from_instance

    @staticmethod
    def option_label_from_instance(obj):
        from django.utils.encoding import smart_text
        return smart_text(obj.short_label)


class TemplateTypeForm(forms.Form):
    from .templates import TEMPLATE_CHOICES

    template_type = forms.ChoiceField(choices=(('', '---------'),) + TEMPLATE_CHOICES)


class CreateTemplateMultiForm(FinancesMultiModelForm):
    form_classes = {
        'account': CreateAccountTemplateForm,
        'bill': CreateBillTemplateForm,
        'template_type': TemplateTypeForm
    }


class UpdateAccountTemplateForm(CreateAccountTemplateForm):
    class Meta(CreateAccountTemplateForm.Meta):
        fields = CreateAccountTemplateForm.Meta.fields + ['disabled']


class UpdateBillTemplateForm(CreateBillTemplateForm):
    class Meta(CreateBillTemplateForm.Meta):
        fields = CreateBillTemplateForm.Meta.fields + ['disabled']


class UpdateTemplateForm(UserAndNameMixin, forms.ModelForm):
    pass
