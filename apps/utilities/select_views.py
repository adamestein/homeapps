from django.http import Http404
from django.shortcuts import redirect

from library.views.generic import AppFormView

from .forms import SelectForm


class SelectView(AppFormView):
    form_class = SelectForm
    select = None
    template_name = 'utilities/select_type.html'

    def form_valid(self, form):
        if self.select == 'data':
            return redirect('utilities:view_data', data_type=form.cleaned_data['selected_type'])
        elif self.select == 'statement':
            return redirect('utilities:add_statement', statement_type=form.cleaned_data['selected_type'])
        else:
            raise Http404(f'Unknown data type: {self.select}')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = self.select.capitalize()
        context['submit_on_select'] = True
        return context

    def get_form_kwargs(self):
        kwargs = super(SelectView, self).get_form_kwargs()
        kwargs['include_empty_choice'] = True
        return kwargs
