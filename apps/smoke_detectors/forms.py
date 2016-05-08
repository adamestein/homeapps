from django import forms

from tekextensions.widgets import SelectWithPopUp

from .models import SmokeDetector


class SmokeDetectorForm(forms.ModelForm):
    class Meta:
        model=SmokeDetector
        widgets = {
            'battery_type': SelectWithPopUp(model='BatteryInfo'),
            'location': SelectWithPopUp
        }

    def __init__(self, *args, **kwargs):
        super(SmokeDetectorForm, self).__init__(*args, **kwargs)
        self.fields['battery_type'].label = 'Battery Type'
