from datetime import date

# noinspection PyPackageRequirements
from dateutil.relativedelta import relativedelta
from easy_pdf.views import PDFTemplateView
from moneyed import Money, USD

from django.db.models import Q
from django.utils.dateformat import DateFormat
from django.views.generic import TemplateView

from .models import Account, AccountTemplate, Bill, BillTemplate, Income, IncomeTemplate, Option, Statement
from .statement_forms import AccountForm, BillForm, IncomeForm

from library.views.generic import AppCreateView, AppDetailView, AppListView, AppUpdateView
from library.views.generic.mixins.ajax import AJAXResponseMixin
from library.views.generic.mixins.auth import LoginRequiredMixin

from django.views.generic.edit import ModelFormMixin, ProcessFormView


class BaseStatementView(ModelFormMixin, ProcessFormView):
    snap_section = None
    success_message = ''

    class Meta:
        abstract = True

    def determine_closest_date(self, target_date):
        prev_dates = []
        current_dates = []
        next_dates = []

        # Create dates based on the snap day settings for the previous, current, and next month. Which every today
        # comes the closest to is the date we'll snap to.
        for day in self.request.user.preference.snap_days.split(','):
            current_dates.append(date(target_date.year, target_date.month, int(day)))
            prev_dates.append(current_dates[-1] - relativedelta(months=1))
            next_dates.append(current_dates[-1] + relativedelta(months=1))

        prev_diff = [abs(calc_date - target_date) for calc_date in prev_dates]
        current_diff = [abs(calc_date - target_date) for calc_date in current_dates]
        next_diff = [abs(calc_date - target_date) for calc_date in next_dates]

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

        return closest_date

    def form_valid(self, multiform):
        statement = multiform.forms['statement'].save()

        self._save_data(statement, multiform.forms['account'], Account)
        self._save_data(statement, multiform.forms['bill'], Bill)
        self._save_data(statement, multiform.forms['income'], Income)

        return super(BaseStatementView, self).form_valid(multiform)

    def get_context_data(self, **kwargs):
        context = super(BaseStatementView, self).get_context_data(**kwargs)
        context.update({
            'account_choices': self._get_account_choices(),
            'bill_choices': self._get_bill_choices(),
            'income_choices': self._get_income_choices()
        })

        return context

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(date=DateFormat(cleaned_data['date']).format('F jS, Y'))

    def _get_account_choices(self):
        return AccountTemplate.objects.filter(user=self.request.user, disabled=False)

    def _get_bill_choices(self):
        snap_section_query = Q(snap_section=self.snap_section) | Q(snap_section=0)
        return BillTemplate.objects.filter(snap_section_query, user=self.request.user, disabled=False)

    def _get_income_choices(self):
        snap_section_query = Q(snap_section=self.snap_section) | Q(snap_section=0)
        return IncomeTemplate.objects.filter(snap_section_query, user=self.request.user, disabled=False)

    @staticmethod
    def _save_data(statement, forms, model):
        saved_ids = []
        for form in forms:
            instance = form.save(commit=False)
            instance.statement = statement
            instance.save()
            option_list = form.cleaned_data.get('option_list', None)
            # Options from the template are stored as a string of joined Option pks, so know we need to add those
            # options (if any) to thew new instance
            if option_list:
                for option_pk in option_list.split(','):
                    instance.options.add(Option.objects.get(pk=option_pk))
            saved_ids.append(instance.id)
        model.objects.filter(statement=statement).exclude(id__in=saved_ids).delete()      # Delete 'deleted' items


class StatementCreateView(BaseStatementView, AppCreateView):
    def get_initial(self):
        return {
            'statement': {
                'date': self.determine_closest_date(date.today())
            }
        }


class StatementDetailView(AppDetailView):
    def get_context_data(self, **kwargs):
        context = super(StatementDetailView, self).get_context_data(**kwargs)

        # Add calculated values to the context
        _calculations(self.object, context)

        return context


class StatementListView(AppListView):
    action = None

    def __init__(self, **kwargs):
        try:
            action = kwargs.pop("action")
        except KeyError:
            raise RuntimeError(
                'StatementListView:__init__(): action must be specified'
            )
        else:
            super(StatementListView, self).__init__(**kwargs)

            self.action = action

    def get_context_data(self, **kwargs):
        context = super(StatementListView, self).get_context_data(**kwargs)
        context.update({
            "action": self.action
        })
        return context


class StatementPDFView(LoginRequiredMixin, PDFTemplateView):
    template_name = 'finances/statement/pdf.html'

    def get_context_data(self, **kwargs):
        statement = Statement.objects.get(pk=kwargs['pk'])

        context = super(StatementPDFView, self).get_context_data(
            object=statement,
            pagesize='letter',
            title='Statement for {}'.format(statement),
            **kwargs
        )

        # Add calculated values to the context
        _calculations(statement, context)

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
                        'option_list': ','.join(str(pk) for pk in template.options.all().values_list('pk', flat=True)),
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
                        'option_list': ','.join(str(pk) for pk in template.options.all().values_list('pk', flat=True))
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
                info = {'button_text': str(form.save(commit=False).create_display)}
            else:
                info = {'errors': str(form)}
        elif table_type == 'income':
            form = IncomeForm(self.request.POST, prefix=prefix)
            if form.is_valid():
                info = {'button_text': str(form.save(commit=False))}
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


class StatementUpdateView(BaseStatementView, AppUpdateView):
    def get_context_data(self, **kwargs):
        self.determine_closest_date(self.object.date)
        return super(StatementUpdateView, self).get_context_data(**kwargs)

    def get_form_kwargs(self):
        kwargs = super(StatementUpdateView, self).get_form_kwargs()
        kwargs.update(instance={
            'account': self.object.account_set.all(),
            'bill': self.object.bill_set.all(),
            'income': self.object.income_set.all(),
            'statement': self.object
        })
        return kwargs

    def get_object(self, queryset=None):
        return Statement.objects.get(pk=self.kwargs.get(self.pk_url_kwarg))


def _calculations(statement, context):
    bills = statement.bill_set.all()
    income = statement.income_set.all()

    bill_sum = sum([bill.amount for bill in bills]) if bills.count() else Money(0, USD)
    income_sum = sum([income.amount for income in income]) if income.count() else Money(0, USD)

    context.update({
        'diff': income_sum - bill_sum,
        'total': {
            'account': sum([account.amount for account in statement.account_set.all()]),
            'bill': bill_sum,
            'income': income_sum
        }
    })
