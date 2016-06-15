from collections import OrderedDict

from betterforms.multiform import MultiModelForm

from django.core.exceptions import ValidationError


class FinancesMultiModelForm(MultiModelForm):
    save_m2m = None

    def get_selected_template(self):
        return self.forms[self.forms.values()[0].cleaned_data['template_type']]

    def is_valid(self):
        template_type = self.forms.values()[0].cleaned_data['template_type']

        # If the TemplateType form is valid, verify that the form it's pointing to is valid. If the other form is
        # also valid, the whole multi form is valid.
        if self.forms.values()[0].is_valid():
            if template_type == 'account':
                forms_valid = self.forms.values()[1].is_valid()
            elif template_type == 'bill':
                forms_valid = self.forms.values()[2].is_valid()
            elif template_type == 'income':
                forms_valid = self.forms.values()[3].is_valid()
            else:
                raise RuntimeError(
                    'FinancesMultiModelForm:is_valid(): unknown template type ({})'.format(template_type)
                )
        else:
            forms_valid = False

        try:
            cleaned_data = self.clean()
        except ValidationError as e:
            self.add_crossform_error(e)
        else:
            if cleaned_data is not None:
                for key, data in cleaned_data.items():
                    self.forms[key].cleaned_data = data
        return forms_valid and not self.crossform_errors

    def save(self, commit=True):
        objects = OrderedDict()
        save_this = self.forms.values()[0].cleaned_data['template_type']

        for key, form in self.forms.items():
            if key == save_this:
                objects[key] = form.save(commit)
            else:
                objects[key] = form

        if any(hasattr(form, 'save_m2m') for form in self.forms.values()):
            def save_m2m():
                for form in self.forms.values():
                    if hasattr(form, 'save_m2m'):
                        form.save_m2m()
            self.save_m2m = save_m2m

        return objects
