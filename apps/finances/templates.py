from .forms import UpdateAccountTemplateForm, UpdateBillTemplateForm
from .models import AccountTemplate, BillTemplate

from library.views.generic import AppCreateView, AppListView, AppUpdateView


class TemplateCreateView(AppCreateView):
    object = None
    success_message = None

    def form_valid(self, form):
        # Save the correct template form (based on the template type chosen)
        self.object = form.get_selected_template().save()

        return super(TemplateCreateView, self).form_valid(form)


class TemplateListView(AppListView):
    def get_context_data(self, **kwargs):
        # Add all the templates so that we can display them all
        context = super(TemplateListView, self).get_context_data(**kwargs)
        context['templates'] = {
            'account': AccountTemplate.objects.exclude(disabled=True),
            'bill': BillTemplate.objects.exclude(disabled=True)
        }
        context['total_templates'] = sum(context['templates'][name].count() for name in context['templates'])

        return context


class TemplateUpdateView(AppUpdateView):
    def get_form_class(self):
        if self.kwargs['template_type'] == 'account':
            return UpdateAccountTemplateForm
        elif self.kwargs['template_type'] == 'bill':
            return UpdateBillTemplateForm
        else:
            raise RuntimeError(
                'TemplateUpdateView.get_form_class(): unknown template type ({})'.format(self.kwargs['template_type'])
            )

    def get_object(self):
        if self.kwargs['template_type'] == 'account':
            return AccountTemplate.objects.get(pk=self.kwargs.get(self.pk_url_kwarg))
        elif self.kwargs['template_type'] == 'bill':
            return BillTemplate.objects.get(pk=self.kwargs.get(self.pk_url_kwarg))
        else:
            raise RuntimeError(
                'TemplateUpdateView.get_object(): unknown template type ({})'.format(self.kwargs['template_type'])
            )