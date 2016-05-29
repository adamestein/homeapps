from django import forms

from .models import AccountTemplate


class AddAccountTemplateForm(forms.ModelForm):
    class Meta:
        fields = ['name', 'account_number']
        model=AccountTemplate


class UpdateAccountTemplateForm(forms.ModelForm):
    class Meta:
        fields = ['name', 'account_number', 'disabled']
        model=AccountTemplate
