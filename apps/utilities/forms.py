from django import forms

from .models import ElectricGasStatement, WaterStatement


class ElectricGasStatementForm(forms.ModelForm):
    class Meta:
        exclude = ('user',)
        model = ElectricGasStatement


class SelectForm(forms.Form):
    selected_type = forms.ChoiceField(
        choices=[
            ('electric_gas', 'Electric & Gas'),
            ('water', 'Water'),
        ],
        label='Type'
    )


class WaterStatementForm(forms.ModelForm):
    class Meta:
        exclude = ('user',)
        model = WaterStatement
