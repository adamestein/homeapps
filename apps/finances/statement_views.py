from datetime import date

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView

from .models import Account, AccountTemplate, Income, IncomeTemplate
from .statement_forms import AccountForm, IncomeForm

from library.views.generic import AppCreateView, AppDetailView
from library.views.generic.mixins.ajax import AJAXResponseMixin


class StatementCreateView(AppCreateView):
    def get_context_data(self, **kwargs):
        context = super(StatementCreateView, self).get_context_data(**kwargs)
        context.update({
            'account_choices': _get_account_choices(self.request.user),
            'income_choices': _get_income_choices(self.request.user)
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

        for form in multiform.forms['income']:
            income = form.save(commit=False)
            income.statement = statement
            income.save()
            form.save_m2m()

        return HttpResponseRedirect(reverse('statement_detail', args=[statement.pk]))


class StatementDetailView(AppDetailView):
    def get_context_data(self, **kwargs):
        context = super(StatementDetailView, self).get_context_data(**kwargs)

        context.update({
            'total': {
                'account': sum([account.amount for account in self.object.account_set.all()]),
                'income': sum([income.amount for income in self.object.income_set.all()])
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
        elif table_type == 'income':
            if pk:
                template = IncomeTemplate.objects.get(pk=pk)
                form = IncomeForm(
                    initial={
                        'account_number': template.account_number,
                        'name': template.name,
                        'options': template.options.all()
                    },
                    prefix=prefix
                )

                if template.arrival_day:
                    today = date.today()
                    form.initial['date'] = date(today.year, today.month, template.arrival_day).strftime('%m/%d/%Y')
            else:
                form = IncomeForm(prefix=prefix)
        else:
            raise RuntimeError('StatementSectionForm:get_context_data(): unknown table type ({})'.format(table_type))

        return {'form': str(form), 'table_type': table_type}


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
                    )
                }
            else:
                info = {'errors': str(form)}
        elif table_type == 'income':
            form = IncomeForm(self.request.POST, prefix=prefix)
            if form.is_valid():
                info = {
                    'button_text': str(
                        Income(
                            account_number=form.cleaned_data['account_number'],
                            amount=form.cleaned_data['amount'],
                            date=form.cleaned_data['date'],
                            name=form.cleaned_data['name']
                        )
                    )
                }
            else:
                info = {'errors': str(form)}
        else:
            raise RuntimeError(
                'StatementSectionFormValidation:get_context_data(): unknown table type ({})'.format(table_type)
            )

        if 'button_text' in info:
            # Add common items that all returned info will have
            info['form'] = form.as_table()
            info['name'] = form.cleaned_data['name']

        return info


def _get_account_choices(user):
    return AccountTemplate.objects.filter(user=user, disabled=False)


def _get_income_choices(user):
    return IncomeTemplate.objects.filter(user=user, disabled=False)
