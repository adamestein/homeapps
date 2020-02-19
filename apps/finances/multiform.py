from collections import OrderedDict

from betterforms.multiform import MultiModelForm

from django.core.exceptions import ValidationError

from .const import TEMPLATE_ACCOUNT_FORM, TEMPLATE_BILL_FORM, TEMPLATE_INCOME_FORM, TEMPLATE_TEMPLATE_TYPE_FORM


class StatementMultiForm(MultiModelForm):
    def get_selected_form(self):
        # Return data from the Statement form
        return list(self.forms.values())[3]

    def is_valid(self):
        forms_valid = all(form.is_valid() for form in self.forms.values())
        try:
            self.clean()
        except ValidationError as e:
            self.add_crossform_error(e)
        return forms_valid and not self.crossform_errors


class TemplateMultiModelForm(MultiModelForm):
    save_m2m = None

    def get_selected_form(self):
        return self.forms[list(self.forms.values())[TEMPLATE_TEMPLATE_TYPE_FORM].cleaned_data['template_type']]

    def is_valid(self):
        form_value_list = list(self.forms.values())

        # If the TemplateType form is valid, verify that the form it's pointing to is valid. If the other form is
        # also valid, the whole multi form is valid.
        if form_value_list[TEMPLATE_TEMPLATE_TYPE_FORM].is_valid():
            template_type = form_value_list[TEMPLATE_TEMPLATE_TYPE_FORM].cleaned_data['template_type']

            if template_type == 'account':
                forms_valid = form_value_list[TEMPLATE_ACCOUNT_FORM].is_valid()
            elif template_type == 'bill':
                forms_valid = form_value_list[TEMPLATE_BILL_FORM].is_valid()
            elif template_type == 'income':
                forms_valid = form_value_list[TEMPLATE_INCOME_FORM].is_valid()
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
        form_value_list = list(self.forms.values())
        objects = OrderedDict()
        save_this = form_value_list[0].cleaned_data['template_type']

        for key, form in list(self.forms.items()):
            if key == save_this:
                objects[key] = form.save(commit)
            else:
                objects[key] = form

        if any(hasattr(form, 'save_m2m') for form in form_value_list):
            def save_m2m():
                for form_values in form_value_list:
                    if hasattr(form_values, 'save_m2m'):
                        form_values.save_m2m()
            self.save_m2m = save_m2m

        return objects
