from tekextensions.widgets import SelectWithPopUp

from django import forms

from .models import BatteryChangeEvent, SmokeDetector


class BatteryChangeEventForm(forms.ModelForm):
    class Meta:
        exclude = []
        model=BatteryChangeEvent
        widgets = {
            'date': forms.DateInput(format='%m/%d/%Y')
        }


class SmokeDetectorForm(forms.ModelForm):
    class Meta:
        exclude = []
        model=SmokeDetector
        widgets = {
            'battery_type': SelectWithPopUp(model='BatteryInfo'),
            'location': SelectWithPopUp
        }

    def __init__(self, *args, **kwargs):
        super(SmokeDetectorForm, self).__init__(*args, **kwargs)
        self.fields['battery_type'].label = 'Battery Type'
