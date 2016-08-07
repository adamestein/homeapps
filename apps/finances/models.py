from datetime import date

from django.contrib.auth.models import User
from django.db import models
from django.utils.dateformat import DateFormat

from djmoney.models.fields import MoneyField

from library.abstract_models import Auth, StatementItem, Template
from library.ordinal import ordinal


class Account(StatementItem, models.Model):
    account_number = models.PositiveIntegerField(
        db_index=True, blank=True, null=True, default='', help_text='Account number.'
    )

    class Meta:
        ordering = ('name', 'statement__date')

    @classmethod
    def str_format(cls, name, account_number, amount, item_date=None):
        acct_num = ' (acct #{})'.format(account_number) if account_number else ''
        date_val = ' as of {}'.format(DateFormat(item_date).format('F jS, Y')) if item_date else ''
        return u'{}{} with {}{}'.format(name, acct_num, amount, date_val)

    def __unicode__(self):
        return Account.str_format(self.name, self.account_number, self.amount, self.statement.date)


class AccountTemplate(Template):
    account_number = models.PositiveIntegerField(
        db_index=True, blank=True, null=True, default='', help_text='Account number.'
    )


class Bill(StatementItem, models.Model):
    account_number = models.PositiveIntegerField(
        db_index=True, blank=True, null=True, default='', help_text='Account number.'
    )
    actual = MoneyField(
        max_digits=10, decimal_places=2, default_currency='USD', blank=True, null=True, help_text='Actual amount paid.'
    )
    date = models.DateField(db_index=True, help_text='Due date.')
    paid_date = models.DateField(blank=True, null=True, help_text='The date the bill was paid')
    total = MoneyField(
        max_digits=10, decimal_places=2, default_currency='USD', blank=True, null=True,
        help_text="Total amount of the bill if 'amount' is partial."
    )
    options = models.ManyToManyField(
        'Option', help_text='Options for the income.', blank=True, limit_choices_to={'template_type': 'bill'}
    )
    url = models.URLField(blank=True, null=True, help_text='Web site URL used to pay this bill.')

    class Meta:
        ordering = ('date', 'name')

    def __unicode__(self):
        total = ' (total is {})'.format(self.total) if self.total else ''

        fstr = '{} for {}{} due on {}'.format(self.name, self.amount, total, DateFormat(self.date).format('F jS, Y'))

        if self.paid_date:
            fstr += ' and paid on ' + DateFormat(self.paid_date).format('F jS, Y')
            fstr += ' ({})'.format(self.actual) if self.actual else ' (PIF)'

        return unicode(fstr)


class BillTemplate(Template):
    account_number = models.PositiveIntegerField(
        db_index=True, blank=True, null=True, default='', help_text="Account number."
    )
    amount = MoneyField(
        max_digits=10, decimal_places=2, default_currency='USD', blank=True, null=True, help_text='Amount of the bill.'
    )
    due_day = models.PositiveSmallIntegerField(
        blank=True, null=True, help_text='Day of the month this bill is due (0 means last day of the month).'
    )
    total = MoneyField(
        max_digits=10, decimal_places=2, default_currency='USD', blank=True, null=True,
        help_text="Total amount of the bill if 'amount' is partial."
    )
    options = models.ManyToManyField(
        'Option', help_text='Options for the bill.', blank=True, limit_choices_to={'template_type': 'bill'}
    )
    snap_section = models.PositiveSmallIntegerField(help_text='Snap section in which this template should be shown')
    url = models.URLField(blank=True, null=True, help_text='Web site URL used to pay this bill.')

    def __unicode__(self):
        fstr = self.name

        if self.amount:
            fstr += ' for {}'.format(self.amount)

        if self.due_day:
            fstr += ' due on the {} of the month'.format(DateFormat(date(1, 1, self.due_day)).format('jS'))

        return unicode(fstr)


class Income(StatementItem, models.Model):
    account_number = models.PositiveIntegerField(
        db_index=True, blank=True, null=True, default='', help_text="Account number."
    )
    date = models.DateField(db_index=True, help_text="Transaction date (date it was deposited).",)
    options = models.ManyToManyField(
        'Option', help_text='Options for the income.', blank=True, limit_choices_to={'template_type': 'income'}
    )

    class Meta:
        ordering = ('date', 'name')

    def __unicode__(self):
        fstr = '{} for {} deposited on {}'.format(self.name, self.amount, DateFormat(self.date).format('F jS, Y'))
        if self.account_number:
            fstr += ' into account #{}'.format(self.account_number)
        return unicode(fstr)


class IncomeTemplate(Template):
    account_number = models.PositiveIntegerField(
        db_index=True, blank=True, null=True, default='', help_text="Account number."
    )
    amount = MoneyField(
        max_digits=10, decimal_places=2, default_currency='USD', blank=True, null=True, help_text='Income amount.'
    )
    arrival_day = models.PositiveSmallIntegerField(
        blank=True, null=True,
        help_text='Day of the month this income is expected to arrive (0 means last day of the month).'
    )
    options = models.ManyToManyField(
        'Option', help_text='Options for the income.', blank=True, limit_choices_to={'template_type': 'income'}
    )
    snap_section = models.PositiveSmallIntegerField(help_text='Snap section in which this template should be shown')


class Option(models.Model):
    from .template_views import TEMPLATE_CHOICES

    template_type = models.CharField(max_length=7, choices=TEMPLATE_CHOICES[1:])    # Don't include 'account'
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100)

    @property
    def short_label(self):
        return u'{} - {}'.format(self.name, self.description)

    def __unicode__(self):
        return u'{}: {} - {}'.format(self.template_type, self.name, self.description)


class Preference(models.Model):
    user = models.OneToOneField(User)
    snap_days = models.CommaSeparatedIntegerField(max_length=5)

    def __unicode__(self):
        days = [int(day) for day in self.snap_days.split(',')]

        if len(days) == 1:
            return u'Snap day set to the {} of the month'.format(ordinal(days[0]))
        else:
            text = 'Snap days set to the '

            if len(days) == 2:
                text += '{} and {}'.format(ordinal(days[0]), ordinal(days[1]))
            else:
                for index, day in enumerate(days):
                    if index == len(days) - 1:
                        text += ', and {}'.format(ordinal(int(day)))
                    elif index:
                        text += ', {}'.format(ordinal(int(day)))
                    else:
                        text += '{}'.format(ordinal(int(day)))

            text += ' of the month'
            return unicode(text)


class Statement(Auth, models.Model):
    date = models.DateField(db_index=True, help_text='Statement date')

    class Meta:
        ordering = ('date', )
        unique_together = (('user', 'date'), )

    def __unicode__(self):
        return unicode(DateFormat(self.date).format('F jS, Y'))
