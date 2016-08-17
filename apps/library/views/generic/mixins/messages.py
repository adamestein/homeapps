from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect


from django.contrib import messages


class AppSuccessMessageMixin(SuccessMessageMixin):
    """
    Adds a success message on successful form submission. Can handle when Multi forms are used.
    """
    request = None

    def form_valid(self, form):
        if hasattr(form, 'forms'):
            # Form is a multi form
            return super(AppSuccessMessageMixin, self).form_valid(form.get_selected_form())
        else:
            return super(AppSuccessMessageMixin, self).form_valid(form)
