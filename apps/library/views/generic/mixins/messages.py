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
            if self.success_message:
                messages.success(self.request, self.success_message % form.get_selected_template().cleaned_data)

            # noinspection PyUnresolvedReferences
            return HttpResponseRedirect(self.get_success_url())
        else:
            return super(AppSuccessMessageMixin, self).form_valid(form)
