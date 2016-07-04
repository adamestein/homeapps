from datetime import date

from django.contrib.auth.models import User
from django.db import models
from django.utils.dateformat import DateFormat

from djmoney.models.fields import MoneyField

from library.abstract_models import Auth, StatementItem, Template


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
        return '{}{} with {}{}'.format(name, acct_num, amount, date_val)

    def __unicode__(self):
        return Account.str_format(self.name, self.account_number, self.amount, self.statement.date)


class AccountTemplate(Template):
    account_number = models.PositiveIntegerField(
        db_index=True, blank=True, null=True, default='', help_text='Account number.'
    )


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
    options = models.ManyToManyField('Option', help_text='Options for the bill.', blank=True)
    url = models.URLField(blank=True, null=True, help_text='Web site URL used to pay this bill.')

    def __unicode__(self):
        fstr = self.name

        if self.amount:
            fstr += ' for {}'.format(self.amount)

        if self.due_day:
            fstr += ' due on the {} of the month'.format(DateFormat(date(1, 1, self.due_day)).format('jS'))

        return fstr


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
    options = models.ManyToManyField('Option', help_text='Options for the income.', blank=True)


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


class Statement(Auth, models.Model):
    date = models.DateField(db_index=True, help_text='Statement date')

    class Meta:
        ordering = ('date', )
        unique_together = (('user', 'date'), )

    def __unicode__(self):
        return DateFormat(self.date).format('F jS, Y')
