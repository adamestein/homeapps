from django import forms
from django.db.models.fields import BLANK_CHOICE_DASH

from .models import ElectricGasStatement, WaterStatement


class ElectricGasStatementForm(forms.ModelForm):
    class Meta:
        exclude = ('user',)
        model = ElectricGasStatement


class SelectForm(forms.Form):
    choices = [
        ('electric_gas', 'Electric & Gas'),
        ('water', 'Water'),
    ]

    selected_type = forms.ChoiceField(
        choices=choices,
        label='Type'
    )

    def __init__(self, *args, **kwargs):
        include_empty_choice = kwargs.pop('include_empty_choice', False)
        super(SelectForm, self).__init__(*args, **kwargs)

        if include_empty_choice:
            self.fields['selected_type'].choices = BLANK_CHOICE_DASH + self.choices


class WaterStatementForm(forms.ModelForm):
    class Meta:
        exclude = ('user',)
        model = WaterStatement
