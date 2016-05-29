from django import forms

from .models import AccountTemplate

from library.mixins.forms import UserAndNameMixin


class AddAccountTemplateForm(UserAndNameMixin, forms.ModelForm):
    class Meta:
        fields = ['name', 'account_number']
        model=AccountTemplate


class UpdateAccountTemplateForm(UserAndNameMixin, forms.ModelForm):
    class Meta:
        fields = ['name', 'account_number', 'disabled']
        model=AccountTemplate
