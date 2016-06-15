from datetime import date

from django.db import models
from django.utils.dateformat import DateFormat
from djmoney.models.fields import MoneyField

from library.abstract_models import Template

# Leave commented out until we have a Statement model in place
# class AccountSummary(models.Model):
#     account = models.ForeignKey("AccountTemplate", help_text="Account template.")
#     amount = MoneyField(help_text='Current amount in this account.')
#     statement = models.ForeignKey("Statement", help_text = "To which statement this account summary belongs.",)


class AccountTemplate(Template):
    account_number = models.PositiveIntegerField(
        db_index=True, blank=True, null=True, default='', help_text="Account number."
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
    from .templates import TEMPLATE_CHOICES

    template_type = models.CharField(max_length=7, choices=TEMPLATE_CHOICES[1:])    # Don't include 'account'
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100)

    @property
    def short_label(self):
        return u'{} - {}'.format(self.name, self.description)

    def __unicode__(self):
        return u'{}: {} - {}'.format(self.template_type, self.name, self.description)
