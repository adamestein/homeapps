from datetime import date

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView

from .models import Account, AccountTemplate
from .statement_forms import AccountForm

from library.views.generic import AppCreateView, AppDetailView
from library.views.generic.mixins.ajax import AJAXResponseMixin


class StatementCreateView(AppCreateView):
    def get_context_data(self, **kwargs):
        context = super(StatementCreateView, self).get_context_data(**kwargs)
        context.update({
            'account_choices': _get_account_choices(self.request.user)
        })

        return context

    @staticmethod
    def get_initial():
        return {
            'statement': {
                'date': date.today().strftime('%m/%d/%Y')
            }
        }

    @staticmethod
    def form_valid(multiform):
        statement = multiform.forms['statement'].save()

        for form in multiform.forms['account']:
            account = form.save(commit=False)
            account.statement = statement
            account.save()

        return HttpResponseRedirect(reverse('statement_detail', args=[statement.pk]))


class StatementDetailView(AppDetailView):
    def get_context_data(self, **kwargs):
        context = super(StatementDetailView, self).get_context_data(**kwargs)

        account_total = sum([account.amount for account in self.object.account_set.all()])

        context.update({
            'total': {
                'account': account_total
            }
        })

        return context


class StatementSectionForm(AJAXResponseMixin, TemplateView):
    def get_context_data(self, **kwargs):
        pk = self.request.POST['pk']
        table_type = self.request.POST['table_type']
        total_forms = self.request.POST['total_forms']
        prefix = '{}-{}'.format(table_type, total_forms)      # Prefix is used to simulate what formset would use

        if table_type == 'account':
            if pk:
                template = AccountTemplate.objects.get(pk=pk)
                form = AccountForm(
                    initial={
                        'account_number': template.account_number,
                        'name': template.name
                    },
                    prefix=prefix
                )
            else:
                form = AccountForm(prefix=prefix)
        else:
            raise RuntimeError('StatementSectionForm:get_context_data(): unknown table type ({})'.format(table_type))

        return {"form": str(form)}


class StatementSectionFormValidation(AJAXResponseMixin, TemplateView):
    def get_context_data(self, **kwargs):
        table_type = self.request.POST['table_type']
        total_forms = self.request.POST['total_forms']
        prefix = '{}-{}'.format(table_type, total_forms)      # Prefix is used to simulate what formset would use

        if table_type == 'account':
            form = AccountForm(self.request.POST, prefix=prefix)
            if form.is_valid():
                info = {
                    'button_text': Account.str_format(
                        form.cleaned_data['name'],
                        form.cleaned_data['account_number'],
                        form.cleaned_data['amount']
                    ),
                    'form': form.as_p(),
                    'name': form.cleaned_data['name']
                }
            else:
                info = {'errors': str(form)}

            return info
        else:
            raise RuntimeError(
                'StatementSectionFormValidation:get_context_data(): unknown table type ({})'.format(table_type)
            )


def _get_account_choices(user):
    return AccountTemplate.objects.filter(user=user, disabled=False)
