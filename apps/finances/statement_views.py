from datetime import date

from dateutil.relativedelta import relativedelta

from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView

from .models import Account, AccountTemplate, Bill, BillTemplate, Income, IncomeTemplate
from .statement_forms import AccountForm, BillForm, IncomeForm

from library.views.generic import AppCreateView, AppDetailView
from library.views.generic.mixins.ajax import AJAXResponseMixin


class StatementCreateView(AppCreateView):
    snap_section = None

    def get_context_data(self, **kwargs):
        context = super(StatementCreateView, self).get_context_data(**kwargs)
        context.update({
            'account_choices': _get_account_choices(self.request.user),
            'bill_choices': _get_bill_choices(self.request.user, self.snap_section),
            'income_choices': _get_income_choices(self.request.user, self.snap_section)
        })

        return context

    def get_initial(self):
        prev_dates = []
        current_dates = []
        next_dates = []
        today = date.today()

        # Create dates based on the snap day settings for the previous, current, and next month. Which every today
        # comes the closest to is the date we'll snap to.
        for day in self.request.user.preference.snap_days.split(','):
            current_dates.append(date(today.year, today.month, int(day)))
            prev_dates.append(current_dates[-1] - relativedelta(months=1))
            next_dates.append(current_dates[-1] + relativedelta(months=1))

        prev_diff = [abs(calc_date - today) for calc_date in prev_dates]
        current_diff = [abs(calc_date - today) for calc_date in current_dates]
        next_diff = [abs(calc_date - today) for calc_date in next_dates]

        values = [min(prev_diff), min(current_diff), min(next_diff)]
        index_min = min(xrange(len(values)), key=values.__getitem__)

        if index_min == 0:
            # Previous month has the closest date
            index_min = min(xrange(len(prev_diff)), key=prev_diff.__getitem__)
            closest_date = prev_dates[index_min]
        elif index_min == 1:
            # Current month has the closest date
            index_min = min(xrange(len(current_diff)), key=current_diff.__getitem__)
            closest_date = current_dates[index_min]
        else:
            # Next month has the closest date
            index_min = min(xrange(len(next_diff)), key=next_diff.__getitem__)
            closest_date = next_dates[index_min]

        # Snap section is 1-based
        self.snap_section = index_min + 1

        return {
            'statement': {
                'date': closest_date.strftime('%m/%d/%Y')
            }
        }

    @staticmethod
    def form_valid(multiform):
        statement = multiform.forms['statement'].save()

        for form in multiform.forms['account']:
            account = form.save(commit=False)
            account.statement = statement
            account.save()

        for form in multiform.forms['bill']:
            bill = form.save(commit=False)
            bill.statement = statement
            bill.save()
            form.save_m2m()

        for form in multiform.forms['income']:
            income = form.save(commit=False)
            income.statement = statement
            income.save()
            form.save_m2m()

        return HttpResponseRedirect(reverse('statement_detail', args=[statement.pk]))


class StatementDetailView(AppDetailView):
    def get_context_data(self, **kwargs):
        context = super(StatementDetailView, self).get_context_data(**kwargs)

        bill_sum = sum([bill.amount for bill in self.object.bill_set.all()])
        income_sum = sum([income.amount for income in self.object.income_set.all()])

        context.update({
            'diff': income_sum - bill_sum,
            'total': {
                'account': sum([account.amount for account in self.object.account_set.all()]),
                'bill': bill_sum,
                'income': income_sum
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
        elif table_type == 'bill':
            if pk:
                template = BillTemplate.objects.get(pk=pk)
                form = BillForm(
                    initial={
                        'account_number': template.account_number,
                        'amount': template.amount,
                        'name': template.name,
                        'options': template.options.all(),
                        'total': template.total,
                        'url': template.url
                    },
                    prefix=prefix
                )

                if template.due_day:
                    today = date.today()
                    form.initial['date'] = date(today.year, today.month, template.due_day).strftime('%m/%d/%Y')
            else:
                form = BillForm(prefix=prefix)
        elif table_type == 'income':
            if pk:
                template = IncomeTemplate.objects.get(pk=pk)
                form = IncomeForm(
                    initial={
                        'account_number': template.account_number,
                        'amount': template.amount,
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
        elif table_type == 'bill':
            form = BillForm(self.request.POST, prefix=prefix)
            if form.is_valid():
                info = {
                    'button_text': str(
                        Bill(
                            account_number=form.cleaned_data['account_number'],
                            amount=form.cleaned_data['amount'],
                            date=form.cleaned_data['date'],
                            name=form.cleaned_data['name'],
                            total=form.cleaned_data['total']
                        )
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


def _get_bill_choices(user, snap_section):
    snap_section_query = Q(snap_section=snap_section) | Q(snap_section=0)
    return BillTemplate.objects.filter(snap_section_query, user=user, disabled=False)


def _get_income_choices(user, snap_section):
    snap_section_query = Q(snap_section=snap_section) | Q(snap_section=0)
    return IncomeTemplate.objects.filter(snap_section_query, user=user, disabled=False)
