from tekextensions.widgets import MultipleSelectWithPopUp

from django import forms

from .models import Option


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
